from product.productPage import ProductPage as Pp
from dalttProduct.productInfo import ProductInfo
from dalttProduct.productImage import ProductImage
from dalttProduct.productSize import ProductSize


class ProductPage(ProductInfo, ProductImage, ProductSize, Pp):

    pass
