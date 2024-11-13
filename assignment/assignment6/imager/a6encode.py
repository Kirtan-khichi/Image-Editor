"""
Steganography methods for the imager application.

This module provides all of the test processing operations (encode, decode) 
that are called by the application. Note that this class is a subclass of Filter. 
This allows us to layer this functionality on top of the Instagram-filters, 
providing this functionality in one application.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

NAME: KIRTAN KHICHI
DATE: 13 April, 2023
"""
import a6filter


class Encoder(a6filter.Filter):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of Filter.  That means it inherits all of the 
    methods and attributes of that class too. We do that separate the 
    steganography methods from the image filter methods, making the code
    easier to read.
    
    Both the `encode` and `decode` methods should work with the most recent
    image in the edit history.
    """
    
    def encode(self, text):
        """
        Returns True if it could hide the text; False otherwise.
        
        This method attemps to hide the given message text in the current 
        image. This method first converts the text to a byte list using the 
        encode() method in string to use UTF-8 representation:
            
            blist = list(text.encode('utf-8'))
        
        This allows the encode method to support all text, including emoji.
        
        If the text UTF-8 encoding requires more than 999999 bytes or the 
        picture does  not have enough pixels to store these bytes this method
        returns False without storing the message. However, if the number of
        bytes is both less than 1000000 and less than (# pixels - 10), then 
        the encoding should succeed.  So this method uses no more than 10
        pixels to store additional encoding information.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns True...)
        # The last paragraph (If the text UTF-8 encoding...)
        # The precondition (text is a string)

        current = self.getCurrent()
        assert isinstance(text, str)
        if len(text) > 1000000 or len(text) > len(current.getData()) - 10:
            # I take 'Fal' as mark to not encode pixel here.
            self._encode_pixel(0, 'F')
            self._encode_pixel(1, 'a')
            self._encode_pixel(2, 'l')

            return False
        for i in range(10, len(text) + 10):
            self._encode_pixel(i, text[i - 10])

        self._encode_mark(text)

        # I take 'Tru' as mark to encode here.
        self._encode_pixel(0, 'T')
        self._encode_pixel(1, 'r')
        self._encode_pixel(2, 'u')
        
        return True

    def decode(self):
        """
        Returns the secret message (a string) stored in the current image. 
        
        The message should be decoded as a list of bytes. Assuming that a list
        blist has only bytes (ints in 0.255), you can turn it into a string
        using UTF-8 with the decode method:
            
            text = bytes(blist).decode('utf-8')
        
        If no message is detected, or if there is an error in decoding the
        message, this method returns None
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns the secret...)
        # The last paragraph (If no message is detected...)

        current = self.getCurrent()
        blist = []
        text = self._decode_pixel(0) == ord('T') and self._decode_pixel(1) == ord('r') and self._decode_pixel(2) == ord('u')
    
        if text:
            limit_text = []       # Accumalator contains bytes.
            for j in range(3, 10):
                limit_text.append(self._decode_pixel(j))

            print(limit_text)

            limit_text_loop = bytes(limit_text).decode('utf-8')   # Contains my encoded message length in string. 

            for i in range(10, int(limit_text_loop) + 10):

                if (self._decode_pixel(i) <= 255):
                    blist.append(self._decode_pixel(i))

                else: 
                    return

            text = bytes(blist).decode('utf-8')
            return text 

        else:
            return


    # HELPER METHODS
    def _decode_pixel(self, pos):
        """
        Return: the number n hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as 
        the last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it. You are allowed to change it.
        # There are no restrictions on how you can change it.
        rgb = self.getCurrent()[pos]
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10


    def _encode_pixel(self, pos, text):
        """
        It set the pixel according to the hidden message.
        
        This function assumes that the value was a 3-digit number encoded as 
        the last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it. You are allowed to change it.
        # There are no restrictions on how you can change it.

        current = self.getCurrent()
        rgb = self.getCurrent()[pos]
        byte = list(text.encode('utf-8'))

        red = rgb[0] - (rgb[0] % 10) + byte[0] // 100
        green = rgb[1] - (rgb[1] % 10) + (byte[0] // 10) % 10
        blue = rgb[2] - (rgb[2] % 10) + (byte[0] % 10)

        red = red if red <= 255 else (red - 10)
        green = green if green <= 255 else (green - 10)
        blue = blue if blue <= 255 else (blue - 10)

        pixel = (red, green, blue)

        current.setPixel(pos // current.getWidth(), pos % current.getWidth(), pixel)

    def _encode_mark(self, text):
        """
        Set the length of text in pixels from position 3 to 10.
        
        This method attempts to hide the given message text lenght in the current 
        image pixel from position 3 to 7.
                    
        Parameter text: a message to hide
        Precondition: text is a string
        """
        current = self.getCurrent()
        mark = (7 - len(str(len(text)))) * '0' + str(len(text))
        print(len(mark))

        for i in range(3, 7 + 3):
            self._encode_pixel(i, mark[i - 3])