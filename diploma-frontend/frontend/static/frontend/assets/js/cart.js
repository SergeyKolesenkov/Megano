console.warn('Корзина загружена.')
var mix = {
    methods: {
        submitBasket() {
            const items = this.basket?.basket_items || [];

            const payload = {

                items: items.map(item => ({
                product_id: item.product.id,
                count: item.count,
                }))
            };


            this.postData('/api/orders/', payload)
                .then(({ data: { orderId } }) => {

                location.assign(`/orders/${orderId}/`);
                })
                .catch(() => {
                console.warn('Ошибка при создании заказа');
                });
            }
    },
    mounted() {},
    data() {
        return {}
    }
}