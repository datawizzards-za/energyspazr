from app import models

class QuotationCharges:
    def __init__(self, products):
        self.products = products

    def get_prices(self):
        best_three_prices = {}
        products = []
        companies = {}
        for product in self.products:
            best_three_prices[models.Dimension.objects.get(
                id=product).product_id] = models.SellingProduct.objects.filter(
                product_id=product).order_by('price')[:3]
            companies[models.Dimension.objects.get(
                id=product).product_id] = []

            for item in models.SellingProduct.objects.filter(
                product_id=product).order_by('price')[:3]:
                company = models.SellingProduct.objects.get(
                    product_id=product,
                    price=item.price)
                companies[models.Dimension.objects.get(
                    id=product).product_id].append(models.SpazrUser.objects.get(
                    user_id=company.user_id))
            products.append(models.Dimension.objects.get(
                id=product).product_id)
        return best_three_prices, products, companies

