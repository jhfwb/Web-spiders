class Test2:
    pass
class Test:
    """这是一个测试类
    Usage::

        >>> import 范本.python注释范本
        >>> Test().test(s='为了掩饰跨行语法，我特地被'+
        ... '劈成两断')
    """
    name="张三"
    """我是属性注解"""
    def test2(self,a,b,c):
        # type: (str,int,Test) -> str
        pass
    def test3(self,s,fontColor,end):
        """打印出有颜色的字体。默认为黑色。打印后返回打印的值。
        :param str s: 需要打印的内容
        :param str fontColor: 颜色可以是以下几种 red | green | yellow | pink | blue | gray | black | cyan
        :param end: 末尾的字符。
        :return: 返回s的值
        """
        pass

    def test(self,c,s="默认值",a="你好"):
        """用于打印 :class:`Test`.

        :param bool c: 打印
        :param s: 打印
        :return: a key code
        :raises ValueError: if the keys cannot be joined

        有几个作用
            * 能够打印
            * 能够 *斜体* 此处加斜体
            1. 读书
            2. 读书
        Examples:
            >>> Test().test(s='你好')
        """
        # A non-dead key cannot be joined
        print(s)
        return Test2()
if __name__ == '__main__':
    Test().test(1,s='你好')
    Test().name
