import os

if __name__ == '__main__':
   i=11
   a={}
   v={}
   def mexec(s,a={},v={}):

      c=4
      exec(s)
      o={'name':00}
      print(locals())
      print(locals()['c'])
      print()
      print(locals()['c'])
      print(locals())
      print(c)
      crc=11
      # print(dir(o))
      # print(globals())
      pass

   mexec("cc=1")
   print(mexec)
   print(locals())
    # os.system('python -m weditor')