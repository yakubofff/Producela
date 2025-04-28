import numpy as np
import random


def random_num(a,b):
  return 0 #random.randint(-2,2)    

def chunk_gen(a,b,c,d,side): # 3 5 7 2 # 2,4,6,8
  def mid(a,b):
    return (a+b)//2+random_num(-1,1)
  # ab
  # dc
  chunk = np.array([[0]*side]*side)
  chunk[0][0], chunk[0][side-1], chunk[side-1][0], chunk[side-1][side-1] = a,b,d,c
  ab = mid(a,b)
  bc = mid(b,c)
  cd = mid(c,d)
  da = mid(d,a)
  midl = (a+b+c+d)//4+random_num(-1,1)
  #print(chunk, ab,bc,cd,da,mid,side)
  if side != 3:
    to = (side+1)//2
    from_ = (side-1)//2
    #print(chunk[0:to, 0:to])
    #print(chunk_gen(a,ab,mid,da,(side+1)//2))
    #print()
    chunk[0:to, 0:to] = chunk_gen(a,ab,midl,da,(side+1)//2)

    #print(chunk[0:to, from_:side])
    #print(chunk_gen(ab,b,bc,mid,(side+1)//2))
    #print()
    chunk[0:to, from_:side] = chunk_gen(ab,b,bc,midl,(side+1)//2)

    #print(chunk[from_:side, 0:to])
    #print(chunk_gen(mid,bc,c,cd,(side+1)//2))
    #print()
    chunk[from_:side, from_:side] = chunk_gen(midl,bc,c,cd,(side+1)//2)

    #print(chunk[from_:side, from_:side])
    #print(chunk_gen(da,mid,cd,d,(side+1)//2))
    chunk[from_:side, 0:to] = chunk_gen(da,midl,cd,d,(side+1)//2)
  else:
    chunk[0][1] = ab
    chunk[1][0] = da
    chunk[1][2] = bc
    chunk[2][1] = cd
    chunk[1][1] = midl
  return chunk

def generate_map(side,chunk_side, max_height):
  heights = np.random.randint(max_height/2, size=(side+2, side+2)) + np.random.randint(max_height/2, size=(side+2, side+2))
  heights_mid = np.array([[0]*(side+1)]*(side+1))
  for y in range(side+1):
    for x in range(side+1):
      heights_mid[x][y] = int((heights[x,y] + heights[x+1,y] + heights[x,y+1] + heights[x+1,y+1])//4) + random.randint(max_height-max_height//4, max_height+max_height//4)
  map = np.array([[0]*(side*chunk_side)]*(side*chunk_side))
  for x in range(side):
    for y in range(side):
      #print(map[chunk_side*x:chunk_side*(x+1)][chunk_side*y:chunk_side*(y+1)])
      #print(x,y)
      map[chunk_side*x:chunk_side*(x+1), chunk_side*y:chunk_side*(y+1)] = chunk_gen(heights_mid[x,y], heights_mid[x,y+1], heights_mid[x+1,y+1], heights_mid[x+1,y],chunk_side)
  return map


