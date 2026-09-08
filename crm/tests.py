from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, CustomerTrash


class CustomerTrashTestCase(TestCase):
    def test_customer_deletion_moves_to_trash(self):
        # 1. Customer yaratamiz
        customer = Customer.objects.create(
            name="Alisher Navoiy",
            phone="+998901234567",
            is_connected=True,
            is_lead=False,
            comment="Bog'lanildi, mahsulotga qiziqish bildirdi.",
        )
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(CustomerTrash.objects.count(), 0)

        # 2. Customer o'chiramiz
        customer.delete()
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(CustomerTrash.objects.count(), 1)

        # 3. Korzinkadagi ma'lumotlarni tekshiramiz
        trash_item = CustomerTrash.objects.first()
        self.assertEqual(trash_item.name, "Alisher Navoiy")
        self.assertEqual(trash_item.phone, "+998901234567")
        self.assertEqual(trash_item.comment, "Bog'lanildi, mahsulotga qiziqish bildirdi.")
        self.assertTrue(trash_item.is_connected)
        self.assertFalse(trash_item.is_lead)
        self.assertFalse(trash_item.is_expired)
        self.assertGreaterEqual(trash_item.days_left, 29)

    def test_customer_trash_restore(self):
        # 1. Customer yaratib o'chiramiz
        customer = Customer.objects.create(
            name="Zulfiya Isroilova",
            phone="+998909876543",
            is_connected=False,
            is_lead=True,
            comment="Toshkent shahridan, ertaga qayta qo'ng'iroq qilish kerak.",
        )
        customer.delete()
        
        trash_item = CustomerTrash.objects.first()
        self.assertIsNotNone(trash_item)

        # 2. Qayta tiklash (restore)
        restored_customer = trash_item.restore()
        
        self.assertEqual(CustomerTrash.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(restored_customer.name, "Zulfiya Isroilova")
        self.assertEqual(restored_customer.phone, "+998909876543")
        self.assertEqual(restored_customer.comment, "Toshkent shahridan, ertaga qayta qo'ng'iroq qilish kerak.")
        self.assertTrue(restored_customer.is_lead)

    def test_root_url_loads_admin(self):
        # Bosh sahifa (/) admin login oynasiga yo'naltirishi (302) yoki ochishi (200) kerak
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

    def test_api_docs_accessible(self):
        # /api/docs Swagger sahifasi ochilishi kerak
        response = self.client.get('/api/docs')
        self.assertEqual(response.status_code, 200)
