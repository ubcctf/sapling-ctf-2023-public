  height = 6
  width = 4
  def rotate(arr):
      for row in range(0,5,2):
          for col in range(0, len(arr[0]), 2):
              top_left = arr[row][col]
              top_right = arr[row][col+1]
              bot_left = arr[row+1][col]
              bot_right = arr[row+1][col+1]
              arr[row][col] = bot_left
              arr[row][col+1] = top_left
              arr[row+1][col+1] = top_right
              arr[row+1][col] = bot_right
  
  def transpose(arr):
      for row in range(height//2):
          for col in range(len(arr[0])):
              arr[row][col], arr[height-1-row][len(arr[0])-1-col] = arr[height-1-row][len(arr[0])-1-col], arr[row][col]
  
  def construct_num(s):
      a0 = 8 if s[0] == ord("#") else 0
      a1 = 4 if s[1] == ord("#") else 0
      a2 = 2 if s[2] == ord("#") else 0
      a3 = 1 if s[3] == ord("#") else 0
      return a0+a1+a2+a3
  
  def make_art(arr):
      s = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x20\x22\x00\x00\x00\x55\x00\x50\x57\x57\x00\x62\x63\x23\x00\x10\x24\x41\x00\x70\x35\x25\x00\x00\x00\x64\x00\x20\x44\x24\x00\x40\x22\x42\x00\x50\x72\x52\x00\x00\x72\x02\x00\x64\x00\x00\x00\x00\x70\x00\x00\x20\x00\x00\x00\x40\x24\x11\x00\x60\x55\x35\x00\x70\x22\x26\x00\x70\x24\x61\x00\x60\x21\x61\x00\x10\x71\x15\x00\x60\x61\x74\x00\x20\x65\x24\x00\x20\x32\x71\x00\x20\x25\x25\x00\x20\x31\x25\x00\x20\x20\x00\x00\x64\x20\x00\x00\x10\x42\x12\x00\x70\x70\x00\x00\x40\x12\x42\x00\x20\x20\x61\x00\x70\x54\x75\x00\x50\x75\x25\x00\x60\x65\x65\x00\x30\x44\x34\x00\x60\x55\x65\x00\x70\x64\x74\x00\x40\x64\x74\x00\x30\x55\x34\x00\x50\x75\x55\x00\x70\x22\x72\x00\x20\x15\x11\x00\x50\x65\x55\x00\x70\x44\x44\x00\x50\x75\x57\x00\x50\x55\x65\x00\x20\x55\x25\x00\x40\x64\x65\x00\x30\x57\x25\x00\x50\x65\x65\x00\x60\x71\x34\x00\x20\x22\x72\x00\x70\x55\x55\x00\x20\x55\x55\x00\x50\x77\x55\x00\x50\x25\x55\x00\x20\x22\x55\x00\x70\x24\x71\x00\x60\x44\x64\x00\x10\x21\x44\x00\x60\x22\x62\x00\x00\x00\x25\x00\x0f\x00\x00\x00\x00\x00\x62\x00\x70\x35\x00\x00\x60\x65\x44\x00\x30\x34\x00\x00\x30\x35\x11\x00\x30\x76\x00\x00\x20\x72\x12\x00\x17\x75\x00\x00\x50\x65\x44\x00\x20\x22\x20\x00\x26\x22\x20\x00\x50\x56\x44\x00\x20\x22\x22\x00\x50\x77\x00\x00\x50\x65\x00\x00\x20\x25\x00\x00\x64\x65\x00\x00\x31\x35\x00\x00\x40\x64\x00\x00\x60\x32\x00\x00\x30\x72\x02\x00\x70\x55\x00\x00\x20\x55\x00\x00\x70\x57\x00\x00\x50\x52\x00\x00\x24\x55\x00\x00\x30\x62\x00\x00\x30\x62\x32\x00\x22\x22\x22\x00\x60\x32\x62\x00'
      font = []
      for i in range(0,len(s), 4):
          num = s[i:i+4]
          font.append(int.from_bytes(num, byteorder="little"))
      for num in font:
          print(hex(num), end=" ")
  
      print(type(font[0]))
      flag = []
      for col in range(0, len(arr[0]), 4):
          num = 0
          for row in range(6):
              num |= (construct_num(arr[row][col:col+4])) << (4*(5-row))
              print(row, col, hex(num))
          print(hex(num))
          flag.append(chr(font.index(num)))
      print("".join(flag))
  
  def print_art(art):
      for row in art:
          print(row.decode("ascii"))
  
  with open("art.txt", "r") as f:
      art = bytearray(f.read(), encoding="ascii")
      art = art.split(b"\n")
      for i in range(1):
          rotate(art)
      transpose(art)
      print("\n\n")
      print_art(art)
      make_art(art)