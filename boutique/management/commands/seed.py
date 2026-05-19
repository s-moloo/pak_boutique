from django.core.management.base import BaseCommand
from boutique.models import Women, Men, Kids, Accessory # Replace 'boutique' with your actual app name if different

class Command(BaseCommand):
    help = 'Seeds the database with initial Indian boutique data'

    def handle(self, *args, **options):
        # Optional: Clear existing data to avoid duplicates if you run this multiple times
        self.stdout.write('Deleting old data...')
        Women.objects.all().delete()
        Men.objects.all().delete()
        Kids.objects.all().delete()
        Accessory.objects.all().delete()

        self.stdout.write('Creating new boutique data...')

        # ── Women's Collection ────────────────────────────────────────────────
        Women.objects.create(
            description='Bridal Silk Lehenga Choli',
            color='Maroon',
            size="Medium",
            price=450.00,
            category='lehengas',
            image='images\maroon_lehenga.jpg'
        )
        Women.objects.create(
            description='Cotton Printed Shalwar Kameez',
            color='Mustard Yellow',
            size="Large",
            price=65.00,
            category='shalwarkameez',
            image='images\yellow_kameez.jpg'
        )
        Women.objects.create(
            description='Banarasi Silk Saree',
            color='Emerald Green',
            size="One Size",
            price=120.00,
            category='sarees',
            image='images\green_saree.jpg'
        )

        # ── Men's Collection ──────────────────────────────────────────────────
        Men.objects.create(
            description='Classic Silk Blend Kurta',
            color='Navy Blue',
            size="Large",
            price=55.00,
            category='kurta',
            image='images/blue_kurta.jpg'
        )
        Men.objects.create(
            description='Embellished Wedding Sherwani',
            color='Ivory',
            size="Medium",
            price=350.00,
            category='sherwani',
            image='images/ivory_sherwani.jpg'
        )
        Men.objects.create(
            description='Textured Nehru Waistcoat',
            color='Charcoal Grey',
            size="Large",
            price=85.00,
            category='waistcoat',
            image='images/grey_waistcoat.jpg'
        )

        # ── Kids' Collection ──────────────────────────────────────────────────
        Kids.objects.create(
            description='Boys Festive Kurta Pajama',
            color='Mint Green',
            size="Small",
            price=40.00,
            category='kidswear',
            image='images/kids_kurta.jpg'
        )
        Kids.objects.create(
            description='Girls Embroidered Lehenga',
            color='Rani Pink',
            size="Small",
            price=50.00,
            category='kidswear',
            image='images/kids_lehenga.jpg'
        )
        Kids.objects.create(
            description='Traditional Mojari Shoes',
            color='Gold',
            size="Small",
            price=25.00,
            category='footwear',
            image='images/kids_shoes.jpg'
        )

        # ── Accessories ───────────────────────────────────────────────────────
        Accessory.objects.create(
            description='Kundan Choker Necklace Set',
            color='Gold/Emerald',
            size="Small", # 0 or a standard number for "One Size"
            price=150.00,
            category='jewelry',
            image='images/kundan_set.jpg'
        )
        Accessory.objects.create(
            description='Embroidered Potli Handbag',
            color='Beige',
            size="Small",
            price=35.00,
            category='handbags',
            image='images/potli_bag.jpg'
        )
        Accessory.objects.create(
            description='Banarasi Silk Dupatta / Scarf',
            color='Royal Blue',
            size="Small",
            price=45.00,
            category='scarves',
            image='images/silk_dupatta.jpg'
        )

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with boutique items!'))