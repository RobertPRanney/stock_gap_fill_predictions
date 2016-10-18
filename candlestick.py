###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# CLASS FILE: candlestick.py
# USAGE: from candlestick import CandleStick
# DESCR: After messing around with all my candle sticks being stored as lists
#        I am frustrated and think I should just make the dumb things a class
#        will hopefully provide some simplicty for using them in the future
# CREATION DATE: 10/10/16
# CHANGE LOG:
#           10/10/16 - File started, although pull some from old abandoned file
#                    -
###--------------------------------------------------------------------------###
import cPickle as pickle

class CandleStick(object):
    """
    DESCR: a class suitable to hold everythin for a candle stick. Original data
           was pulled down as a list of [open, high, low, close]
    """

    def __init__(self, open_price, high, low, close_price):
        """
        DESCR: initialize a new candlestick object
        INPUT:
            open - float - price candle opened at
            high - float - highest point reached
            low - float - lowest point reached
            close - float - price candle closed at
        OUTPUT: None
        """
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close_price = close_price

    def __str__(self):
        """
        DESCR: Pretty represenation of candlestick
        INPUT: None
        OUTPUT: None
        """
        return "Open: {}, High: {}, Low: {}, Close: {}".format(self.open_price,
                                                               self.high,
                                                               self.low,
                                                               self.close_price)

    def __add__(self, num_or_cand):
        """
        DESCR: Allows candle1 + num
        """
        if type(num_or_cand) == int or type(num_or_cand) == float:
            num = num_or_cand
            return CandleStick(self.open_price + num,
                               self.high + num,
                               self.low + num,
                               self.close_price + num)
        else:
            cand = num_or_cand
            return CandleStick(self.open_price + cand.open_price,
                               self.high + cand.high,
                               self.low + cand.low,
                               self.close_price + cand.close_price)

    def __sub__(self, num_or_cand):
        """
        DESCR: Allows candle1 - num
        """
        if type(num_or_cand) == int or type(num_or_cand) == float:
            num = num_or_cand
            return CandleStick(self.open_price - num,
                               self.high - num,
                               self.low - num,
                               self.close_price - num)
        else:
            cand = num_or_cand
            return CandleStick(self.open_price - cand.open_price,
                               self.high - cand.high,
                               self.low - cand.low,
                               self.close_price - cand.close_price)

    def __mul__(self, num):
        """
        DESCR: Allows candle1 * num
        """
        return CandleStick(self.open_price * num,
                           self.high * num,
                           self.low * num,
                           self.close_price * num)

    def __div__(self, num):
        """
        DESCR: Allows candle1 / num
        """
        return CandleStick(self.open_price / num,
                           self.high / num,
                           self.low / num,
                           self.close_price / num)

    def __iter__(self):
        data = [self.open_price, self.high, self.low, self.close_price]
        for elem in data:
            yield elem

    def is_gain(self):
        """
        DESCR: returns True is net gain (green)
        """
        return True if self.close_price > self.open_price else False

    def is_loss(self):
        """
        DESCR: returns True is net loss (red)
        """
        return True if self.close_price < self.open_price else False

    def is_no_gain(self):
        """
        DESCR: returns True if flat
        """
        return True if self.close_price == self.open_price else False

    def shift_to_zero(self, in_place=False):
        """
        DESCR: move candle down to zero for comparison
        """
        if in_place:
            self.open_price -= self.low
            self.high -= self.low
            self.close -= self.low
            self.low = 0
            return None
        else:
            return self - self.low

    def total_length(self):
        """
        DESCR: Length from bottom tip to top
        """
        return self.high - self.low

    def body_length(self):
        """
        DESCR: just size of body
        """
        return self.close_price - self.open_price

    def __truediv__(self, num):
        """
        DESCR: Allows candle1 / num
        """
        return CandleStick(self.open_price / num,
                           self.high / num,
                           self.low / num,
                           self.close_price / num)


if __name__ == '__main__':
    """
    DESCR: Test code of candlestick class
    """

    test1 = CandleStick(25.1, 55, 20, 28)
    test2 = CandleStick(6, 5, 4, 3)

    print "Open is : {}".format(test1.open_price)
    print "High is: {}".format(test1.high)
    print "Low is: {}".format(test1.low)
    print "Close is: {}".format(test1.close_price)

    print test1
    print test1 + 5
    print test1 - 5
    print test1 * 5
    print test1 / 5
    print test1 + test2
    print test1 - test2
    print test1.is_gain()
    print test2.is_gain()
    print test1.shift_to_zero()

    print "Iter Testing :"
    for item in test1:
        print item

    print "Pickle Test"
    f = open('pickle_test.pkl', 'w')
    pickle.dump(test1, f)
    f.close()

    f = open('pickle_test.pkl', 'r')
    un_pickled = pickle.load(f)
    f.close()

    print un_pickled
