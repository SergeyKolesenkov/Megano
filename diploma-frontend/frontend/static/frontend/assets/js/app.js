const { createApp } = Vue
createApp({
	delimiters: ['${', '}$'],
	mixins: [window.mix ? window.mix : {}],
	methods: {
		getCookie(name) {
			let cookieValue = null
			if (document.cookie && document.cookie !== '') {
				const cookies = document.cookie.split(';')
				for (let i = 0; i < cookies.length; i++) {
					const cookie = cookies[i].trim()
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) === name + '=') {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
						break
					}
				}
			}
			return cookieValue
		},
		postData(url, payload, headers = {}) {
            return axios
                .post(url, payload, {
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken'),
                        ...(headers || {}),
                    },
                })
                .then((response) => {
                    return {
                        data: response?.data,
                        status: response.status,
                    }
                })
				.catch((error) => {
					console.warn(
						`Метод '${url}' вернул статус код ${error.response.status}`
					)
					throw new Error()
				})
		},
		getData(url, payload) {
			return axios
				.get(url, { params: payload })
				.then((response) => {
					return response.data ? response.data : response.json?.()
				})
				.catch(() => {
					console.warn('Метод ' + url + ' не реализован')
					throw new Error('no "get" method')
				})
		},
		search() {
			location.assign(`/catalog/?filter=${this.searchText}`)
		},
		getCategories() {
			this.getData('/api/categories/')
				.then((data) => (this.categories = data))
				.catch(() => {
					console.warn('Ошибка получения категорий')
					this.categories = []
				})
		},
		getBasket() {
        this.getData('/api/cart/')
            .then((data) => {
            this.basket = data
                if (!this.basket || !this.basket.basket_items) {
                    this.basket = { basket_items: [] }
                }
            })
            .catch(() => {
            console.warn('Ошибка при получении корзины')
            this.basket = {
                id: null,
                count: 0,
                total_quantity: 0,
                basket_items: [],
                basketCount: { price: 0 }
            }
            })
        },

        getSales(page = 1) {
            const url = new URL('/api/sales/', window.location.origin);
            url.searchParams.set('currentPage', page);

            fetch(url.toString(), {
                headers: {
                    'Accept': 'application/json',
                },
            })
            .then(res => res.json())
            .then(data => {
                this.salesCards = data.items;
                this.currentPage = data.currentPage;
                this.lastPage = data.lastPage;
            })
            .catch(err => console.error(err));
        },

        changeItemCount(item, delta) {
            const newCount = item.count + delta;

            if (newCount <= 0) {
                this.removeFromBasket(item.id);
            } else {

                axios.patch(`/api/basket/${item.id}/`, { count: newCount }, {
                    headers: { 'X-CSRFToken': this.getCookie('csrftoken') }
                })
                .then(() => this.getBasket())
                .catch(console.error);
            }
        },
		// getLastOrder() {
		// 	this.getData('/api/orders/active/')
		// 		.then(data => {
		// 			this.order = {
		// 				...this.order,
		// 				...data
		// 			}
		// 		})
		// 		.catch(() => {
		// 			console.warn('Ошибка при получении активного заказа')
		// 			this.order = {
		// 				...this.order,
		// 			}
		// 		})
		// },
        getOrder(orderId) {
			if (typeof orderId !== 'number') return
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
					if (typeof data.paymentError !== 'undefined') {
						this.paymentError = data.paymentError
					}
				})
				.catch(err => {
					print.warn("Ошибка при получении деталей заказа", err)
				})
		},
		addToBasket(item, count = 1) {
            this.postData('/api/basket/', {
                product_id: item.id,
                count: count
            })
            .then(({ data }) => {
                this.getBasket();
                alert('Товар добавлен в корзину')
                console.log('Товар успешно добавлен');
            })
            .catch(error => {
                const data = error.response?.data;
                if (data && data.error) {
                    if (data.error.includes('Недостаточно')) {
                        const available = data.available;
                        const canAddMore = data.can_add_more;
                        if (canAddMore > 0) {
                        alert(`На складе всего ${available} шт. Вы можете добавить еще ${canAddMore} шт.`);
                        } else {
                            alert('Товар закончился! Нельзя добавить в корзину.');
                        }
                    } else {
                    console.error('Другая ошибка:', data);
                    alert('Произошла ошибка при добавлении товара. Попробуйте позже.');
                }
                } else {
                console.error('Неизвестный формат ошибки', error);
                alert('Ошибка добавления товара.');
                }
              });
            },
		removeFromBasket(itemId) {
            console.log('ItemID', itemId)
			axios
				.delete(`/api/basket/${itemId}/`, {
					// data: JSON.stringify({ itemId }),
					headers: {
						'X-CSRFToken': this.getCookie('csrftoken'),
						'Content-Type': 'application/json',
					},
				})
				.then(({ data }) => {
					this.getBasket()
				})
				.catch(() => {
					console.warn('Ошибка при удалении заказа из корзины')
				})
		},
		signOut() {
			this.postData('app/sign-out/').finally(() => {
				location.assign(`/`)
			})
		},
        submitPayment() {
			const path = location.pathname;
			const match = path.match(/\/(\d+)\/?$/);
			const orderId = match ? Number(match[1]) : this.orderId;

			if (!orderId) {
				alert('ID заказа не найден');
				return;
			}

			const payload = {
				number: this.number1,
				month: this.month,
				year: this.year,
				code: this.code,
				name: this.name
			};

			console.log('Отправка оплаты для заказа:', orderId, payload);

			this.postData(`/api/payment/${orderId}/`, payload)
				.then(() => {
					alert('Оплата прошла успешно!');
					location.assign('/');
				})
				.catch(err => {
					console.error('Ошибка при оплате:', err);
					alert('Ошибка проведения платежа. Проверите консоль.');
				});
		},
        getOrdersHistory() {
			this.getData('/api/orders/')
				.then((data) => {
					// Записываем полученный массив заказов в переменную orders
					this.orders = data;
					console.log('📜 История заказов успешно загружена:', data);
				})
				.catch(() => {
					console.warn('Ошибка при получении истории заказов');
					this.orders = [];
				});
		},
        confirmOrder() {
			if (!this.basket || !this.basket.id) {
				alert('Корзина пуста или не инициализирована');
				return;
			}
			if (!this.fullName || !this.phone) {
				alert('Заполните имя и телефон');
				return;
			}

			const payload = {
				fullName: this.fullName,
				phone: this.phone,
				email: this.email || '',
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
						alert('Заказ создан, но не получен ID. Проверьте консоль.');
						return;
					}
					console.log('✅ Заказ создан, переход на оплату:', orderId);
					location.replace(`/payment/${orderId}/`);
				})
				.catch(err => {
					console.error('❌ Ошибка оформления заказа', err);
					alert('Не удалось оформить заказ. Проверьте вкладку Network.');
				});
		},
	},
	computed: {
    basketCount() {
        if (!this.basket || !this.basket.basket_items) {
        return { count: 0, price: 0 }
        }
        const items = this.basket.basket_items
        return items.reduce(
        (acc, item) => {
            acc.count += item.count
            acc.price += item.count * (item.product?.price || 0)
            return acc
        },
        { count: 0, price: 0 }
        )
    },
    },
	data() {
		return {
            salesCards: [],
		    currentPage: 1,
		    lastPage: 1,
			// catalog page
			filters: {
				price: {
					minValue: 1,
					maxValue: 500000,
					currentFromValue: 7,
					currentToValue: 27,
				},
			},
			sortRules: [
				{ id: 'rating', title: 'Популярности' },
				{ id: 'price', title: 'Цене' },
				{ id: 'reviews', title: 'Отзывам' },
				{ id: 'date', title: 'Новизне' },
			],
			topTags: [],
			// reused data
			categories: [],
			// reused data
			catalogFromServer: [],
			orders: [],
			cart: [],
			paymentData: {},
			basket: {},
			// order: {
			// 	orderId: null,
			// 	createdAt: '',
			// 	products: [],
			// 	fullName: '',
			// 	phone: '',
			// 	email: '',
			// 	deliveryType: '',
			// 	city: '',
			// 	address: '',
			// 	paymentType: '',
			// 	totalCost: 0,
			// 	status: ''
			// },
			searchText: '',
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
            number1: '',
			month: '',
			year: '',
			code: '',
			name: ''
		}
	},
	mounted() {
		this.getCategories()
		this.getBasket()
        this.getSales()
		// this.getLastOrder()
        const path = location.pathname;
        if (path.includes('history')) {
            this.getOrdersHistory();
        }
        const match = path.match(/\/(\d+)\/?$/);
        if (match) {
            this.orderId = Number(match[1]);
            this.getOrder(this.orderId);
        }
	},
}).mount('#site')

