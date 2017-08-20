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
                dimension_id=product).order_by('price')[:3]
            companies[models.Dimension.objects.get(
                id=product).product_id] = []

            for item in models.SellingProduct.objects.filter(
                    dimension_id=product).order_by('price')[:3]:
                company = models.SellingProduct.objects.get(
                    dimension_id=product,
                    price=item.price)
                companies[models.Dimension.objects.get(
                    id=product).product_id].append(models.SpazrUser.objects.get(
                    user_id=company.user_id))
            products.append(models.Dimension.objects.get(
                id=product).product_id)
        print products, companies
        return best_three_prices, products, companies


class QuotationChargesGeyser:
    def __init__(self, product):
        self.product = product

    def get_prices(self):
        best_three_prices = models.SellingProduct.objects.filter(
                dimension_id=self.product).order_by('price')[:3]
        companies = []
        for item in best_three_prices:
            company = models.SellingProduct.objects.get(
                    dimension_id=self.product,price=item.price)
            companies.append(models.SpazrUser.objects.get(
                    user_id=company.user_id))
        product = models.Dimension.objects.get(
            id=self.product).product_id
        return best_three_prices, product, companies