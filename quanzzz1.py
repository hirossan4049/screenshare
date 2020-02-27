import time
import numpy as np
import Quartz.CoreGraphics as CG

t = time.time()
image = CG.CGWindowListCreateImage(CG.CGRectInfinite, CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID, CG.kCGWindowImageDefault)
prov = CG.CGImageGetDataProvider(image)
_data = CG.CGDataProviderCopyData(prov)
print(time.time() - t)
# width = CG.CGImageGetWidth(image)
# height = CG.CGImageGetHeight(image)
#
# imgdata=np.fromstring(_data,dtype=np.uint8).reshape(len(_data)/4,4)
# numpy_img = imgdata[:width*height,:-1].reshape(height,width,3)