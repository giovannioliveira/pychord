import hashlib

class Key(object):

    def __init__(self, value):
        self.value = value
        self.idlength = 256

    def __repr__(self):
        return self.value[:9]

    def __gt__(self, value):
        if isinstance(value, str):
            return self.value > value
        elif isinstance(value,  Key):
            return  self.value > value.value
        else:
            raise TypeError("__gt__ only supports str or Key as input")

    def __ge__(self, value):
        if isinstance(value, str):
            return self.value >= value
        elif isinstance(value,  Key):
            return  self.value >= value.value
        else:
            raise TypeError("__gt__ only supports str or Key as input")

    def __lt__(self, value):
        if isinstance(value, str):
            return self.value < value
        elif isinstance(value,  Key):
            return  self.value < value.value
        else:
            raise TypeError("__lt__ only supports str or Key as input")

    def __le__(self, value):
        if isinstance(value, str):
            return self.value >= value
        elif isinstance(value,  Key):
            return  self.value >= value.value
        else:
            raise TypeError("__gt__ only supports str or Key as input")

    def __eq__(self, value):
        if isinstance(value, str):
            return self.value == value
        elif isinstance(value,  Key):
            return  self.value == value.value
        else:
            raise TypeError("__eq__ only supports str or Key as input")

    def __ne__(self, value):
        if isinstance(value, str):
            return self.value != value
        elif isinstance(value,  Key):
            return  self.value != value.value
        else:
            raise TypeError("__ne__ only supports str or Key as input")

    def canonicalize(self, value):
        '''
        Returns the str repr of hexa value with the right number of hexa char
        Basically padd the input with'0' and get rid of '0x' and 'L'
        '''
        return format(value, '0>{}x'.format(self.idlength/4))
        
    def __add__(self, value):
        if isinstance(value, int) or isinstance(value, long):
            return self.sumint(value)
        elif isinstance(value, str):
            return self.sumhex(value)
        elif isinstance(value, Key):
            return self.sumhex(value.value)
        else:
            #self.log.error("Sum with unknow type")
            print type(value)
            raise TypeError
    
    def sumint(self, value):
        '''
        Return sum uid + value in hexa representation
        @param value: int to sum with uid value
        '''
        res = (int(self.value, 16) + value) % pow(2, self.idlength)
        return self.canonicalize(res)

    def sumhex(self, value):
        res = (int(self.value, 16) + int(value, 16)) % pow(2, self.idlength)
        return self.canonicalize(res)

    def __sub__(self, value):
        if isinstance(value, int):
            return self.subint(value)
        elif isinstance(value, str):
            return self.subhex(value)
        elif isinstance(value, Key):
            return self.subhex(value.value)
        else:
            #self.log.error("Sub with unknow type")
            raise TypeError
    
    def subint(self, value):
        '''
        Return sub uid - value in hexa representation
        @param value: int to sub with uid value
        '''
        res = (int(self.value, 16) - value) % pow(2, self.idlength)
        return self.canonicalize(res)

    def subhex(self, value):
        '''
        Return sub uid - value in hexa representation
        @param value: str repr of hexa number
        '''
        res = (int(self.value, 16) - int(value, 16)) % pow(2, self.idlength)
        return self.canonicalize(res)

    def __len__(self):
        return len(self.value)
    
    # TODO optim : each isbetween call will be a RPC, sad if we locally know the value of remote node ?
    def isbetween(self, limit1, limit2):
        '''
        Returns True if self.value is contained by [limit1,  limit2]
        Raise exception if limit1 == limit2
        '''
        if len(self.value) != len(limit1) != len(limit2):
            #self.log.error("Unable to compare.")
            raise Exception
        if self.value == limit1 or self.value == limit2:
            return True

        if limit1 > limit2:
            if self.value > limit1 or self.value < limit2:
                return True
            else:
                return False
        elif limit1 < limit2:
            if self.value > limit1 and self.value < limit2:
                return True
            else:
                return False
        else:
            # limit1 == limit2
            raise Exception

class Uid(Key):
    
    def __init__(self, strtohash):
        hash = hashlib.sha256(strtohash)
        Key.__init__(self, hash.hexdigest())
