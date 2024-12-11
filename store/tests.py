from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Review, Product, Category
from django.test import TestCase
from django.urls import reverse


class ReviewModelTest(TestCase):

    def setUp(self):
        # nuovo utente per il test
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category = Category.objects.create(name="Test Category")


        # nuovo prodotto
        self.product = Product.objects.create(
            name="Test Product",
            description= self.category,
            added_by=self.user
        )

        # recensione
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            review="Great product!",
            rating=4.5,
            ip="192.168.0.1"
        )

    def test_review_creation(self):
        # verifica che la recensione sia stata creata correttamente
        review = self.review
        self.assertEqual(review.product.name, "Test Product")
        self.assertEqual(review.user.username, "testuser")
        self.assertEqual(review.review, "Great product!")
        self.assertEqual(review.rating, 4.5)
        self.assertEqual(review.ip, "192.168.0.1")
        self.assertTrue(review.status)

    def test_string_representation(self):
        # verifica la corretta rappresentazione della stringa
        self.assertEqual(str(self.review), "Test Product")

    def test_review_status_default(self):
        # verifica che lo stato di default sia True
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            review="Another great product!",
            rating=5.0,
            ip="192.168.0.2"
        )
        self.assertTrue(review.status)

    def test_review_association_with_product(self):
        # verifica che la recensione sia correttamente associata al prodotto
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            review="Excellent product!",
            rating=4.8,
            ip="192.168.0.4"
        )
        self.assertEqual(review.product, self.product)

    def test_review_association_with_user(self):
        # verifica che la recensione sia correttamente associata all'utente
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            review="Not bad",
            rating=3.0,
            ip="192.168.0.5"
        )
        self.assertEqual(review.user, self.user)

    def test_review_update_at_field(self):
        # verifica che il campo update_at venga aggiornato automaticamente
        review = self.review
        old_update_at = review.update_at

        # modifica il campo review per forzare un salvataggio
        review.review = "Updated review"
        review.save()

        # ricarica l'oggetto dal database per ottenere i valori più aggiornati
        review.refresh_from_db()

        # verifica che `update_at` sia stato effettivamente aggiornato
        self.assertNotEqual(review.update_at, old_update_at)



# test store.views Register_Buyer
class RegisterBuyerTestCase(TestCase):

    def test_register_buyer_get(self):
        response = self.client.get(reverse('register_buyer'))

        # Verifica che la risposta abbia successo
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_buyer.html')
        self.assertContains(response, 'name="username"')

    def test_register_buyer_post_valid(self):

        # login con l'utente appena creato
        self.client.login(username='testuser', password='password123')

        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com',
        }

    # verifica che il modulo venga invalidato correttamente
    def test_register_buyer_post_invalid(self):
        data = {
            'username': '',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'invalidemail',
        }

        response = self.client.post(reverse('register_buyer'), data)

        # verifica che il form non sia valido
        self.assertFalse(response.context['form'].is_valid())

        # verifica che ci siano errori sul campo username
        self.assertTrue(response.context['form'].errors['username'])

        # verifica che ci siano errori sul campo email
        self.assertTrue(response.context['form'].errors['email'])

    # Verifica che l'utente venga avvisato se il nome utente esiste già
    def test_register_buyer_post_existing_user(self):

        # Creiamo un utente esistente
        existing_user = get_user_model().objects.create_user(username='testuser', password='password123')

        data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com',
        }

        response = self.client.post(reverse('register_buyer'), data)

        # Verifica che la risposta sia 200 (l'utente è rimasto sulla stessa pagina)
        self.assertEqual(response.status_code, 200)

        # Verifica che ci siano messaggi di errore
        messages = list(response.context['messages'])
        self.assertTrue(any(msg.message == "Si è verificato un problema con la registrazione. Per favore riprova.." for msg in messages))






