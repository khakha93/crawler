from product.productPage import ProductPage as Pp
from .productInfo import ProductInfo
from .productImage import ProductImage
from .productSize import ProductSize


class ProductPage(ProductInfo, ProductImage, ProductSize, Pp):

    pass
