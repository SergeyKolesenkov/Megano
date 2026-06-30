var mix = {
	methods: {
		getOrder(orderId) {
			if(typeof orderId !== 'number') return
			this.getData(`/api/orders/${orderId}/`)
				.then(data => {
					this.orderId = data.id
					this.createdAt = data.createdAt
					this.fullName = data.fullName
					this.phone = data.phone
					this.email = data.email
					this.deliveryType = data.deliveryType
					this.city = data.city
					this.address = data.address
					this.paymentType = data.paymentType
					this.status = data.status
					this.totalCost = data.totalCost
					this.products = data.products
					console.log(this.products)
					if (typeof data.paymentError !== 'undefined') {
						this.paymentError = data.paymentError
					}
				})
		},
		confirmOrder() {
            // 1. Проверяем, что корзина вообще есть и у неё есть ID
            if (!this.basket || !this.basket.id) {
                alert('Корзина пуста или не инициализирована');
                return;
            }

            // 2. Обязательные поля
            if (!this.fullName || !this.phone) {
                alert('Заполните имя и телефон');
                return;
            }

            const payload = {
                fullName: this.fullName,
                phone: this.phone,
                email: this.email || '',

                // Адрес и доставка — как есть
                city: this.city,
                address: this.address,
                deliveryType: this.deliveryType,
                paymentType: this.paymentType,
                basketId: this.basket.id
            };

            this.postData('/api/orders/', payload)
                .then(({ data }) => {
                    const orderId = data.orderId || data.id;
                    if (!orderId) {
                        console.error('Сервер не вернул ID заказа', data);
                        alert('Заказ создан, но не получен ID. Проверьте консоль.');
                        return;
                    }

                    console.log('✅ Заказ создан, переход на оплату:', orderId);
                    location.replace(`/payment/${orderId}/`);
                })
                .catch(err => {
                    console.error('❌ Ошибка оформления заказа', err);
                    alert('Не удалось оформить заказ. Проверьте консоль (F12 → Network).');
                });
        },

		auth() {
			const username = document.querySelector('#username').value
			const password = document.querySelector('#password').value
			this.postData('/api/sign-in/', JSON.stringify({ username, password }))
				.then(({ data, status }) => {
					location.assign(`/orders/${this.orderId}/`)
				})
				.catch(() => {
					alert('Ошибка авторизации')
				})
		}
	},
	mounted() {
		const path = location.pathname;
        const match = path.match(/\/(\d+)\/?$/);
        if (match) {
            this.orderId = Number(match[1]);
            this.getOrder(this.orderId);
        }
    },
    data() {
		return {
			orderId: null,
			createdAt: '',
			fullName: '',
			phone: '',
			email: '',
			deliveryType: 'ordinary',
			city: '',
			address: '',
			paymentType: 'online',
			status: '',
			totalCost: 0,
			products: [],
			paymentError: null,
			basket: {
				id: null,
				basket_items: []
			}
		};
	},
};