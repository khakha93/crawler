from product.productPage import ProductPage as Pp
from uniqloProduct.productInfo import ProductInfo
from uniqloProduct.productImage import ProductImage
from uniqloProduct.productSize import ProductSize


class ProductPage(ProductInfo, ProductImage, ProductSize, Pp):
    pass