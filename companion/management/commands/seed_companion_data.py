from django.core.management.base import BaseCommand
from companion.models import Partner, Itinerary, ItineraryDay, ItineraryStop, NFCTag, EmergencyContact, FAQ, TravelTip, Announcement
from destinations.models import Destination


class Command(BaseCommand):
    help = "Seed initial NFC tags, itineraries, stops, partners, and emergency contacts for Ratnagiri"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Ratnagiri Companion data...")

        # 0. Top Ratnagiri Destinations
        destinations_data = [
            {
                'title': 'Ratnadurg Fort (Bhagwati Durg)',
                'slug': 'ratnadurg-fort',
                'category': 'Fort',
                'location_name': 'Killa, Ratnagiri',
                'latitude': 16.9856,
                'longitude': 73.2678,
                'description': 'A historic horseshoe-shaped sea fort built by the Bahmani Sultans and fortified by Chhatrapati Shivaji Maharaj, surrounded on three sides by the Arabian Sea.',
                'best_time_to_visit': 'October to March (Sunset: 5:00 PM - 6:30 PM)',
                'travel_tips': 'Wear comfortable walking shoes. The walk along the ramparts offers panoramic sea views and lighthouse views.',
                'entry_fees': 'Free',
                'timings': '06:00 AM - 07:00 PM',
                'is_verified': True,
            },
            {
                'title': 'Ganpatipule Beach & Swayambhu Ganesh',
                'slug': 'ganpatipule-beach-temple',
                'category': 'Temple',
                'location_name': 'Ganpatipule, Ratnagiri (25 km north)',
                'latitude': 17.1458,
                'longitude': 73.2644,
                'description': 'A revered 400-year-old self-manifested (Swayambhu) monolith idol of Lord Ganesha situated right on the pristine white sand shores of Ganpatipule.',
                'best_time_to_visit': 'Year-round; early morning or evening sunset',
                'travel_tips': 'Pradakshina around the hill (1 km) is auspicious. Avoid swimming during high tide as currents can be strong.',
                'entry_fees': 'Free (Special Darshan passes available)',
                'timings': '05:00 AM - 09:00 PM',
                'is_verified': True,
            },
            {
                'title': 'Thibaw Palace & Heritage Museum',
                'slug': 'thibaw-palace',
                'category': 'Viewpoint',
                'location_name': 'Thibaw Point, Ratnagiri',
                'latitude': 16.9935,
                'longitude': 73.3087,
                'description': 'The three-storey red-brick royal palace where King Thibaw and Queen Supayalat of Burma were exiled under British rule from 1886 to 1916. Offers sunset views from Thibaw Point.',
                'best_time_to_visit': 'October to February',
                'travel_tips': 'Visit the museum inside to view ancient Burmese artifacts, coins, and royal photographs.',
                'entry_fees': '₹20 per adult, ₹10 per child',
                'timings': '10:00 AM - 05:30 PM (Closed Mondays)',
                'is_verified': True,
            },
            {
                'title': 'Jaigad Fort & Coastal Lighthouse',
                'slug': 'jaigad-fort-lighthouse',
                'category': 'Fort',
                'location_name': 'Jaigad Village, Ratnagiri (40 km north)',
                'latitude': 17.3006,
                'longitude': 73.2197,
                'description': 'Perched at the mouth of the Shastri River where it joins the Arabian Sea, this 16th-century fortress offers unmatched vantage points over the deep-water bay and British-era lighthouse.',
                'best_time_to_visit': 'Morning or late afternoon',
                'travel_tips': 'Check out the British cast-iron lighthouse nearby, operational since 1899.',
                'entry_fees': 'Free (Lighthouse ₹10)',
                'timings': '06:00 AM - 06:30 PM (Lighthouse: 4:00 PM - 5:30 PM)',
                'is_verified': True,
            },
            {
                'title': 'Mandvi Beach (Black Sand Gateway)',
                'slug': 'mandvi-beach',
                'category': 'Beach',
                'location_name': 'Mandvi, Ratnagiri City',
                'latitude': 16.9833,
                'longitude': 73.2842,
                'description': 'Known as the Gateway of Ratnagiri, Mandvi is famous for its unique dark black sand, gentle waves, and the Rajiwada jetty at the river confluence.',
                'best_time_to_visit': 'Evenings for street food, chana jor garam, and sea breezes',
                'travel_tips': 'A great spot for quick family walks right inside Ratnagiri town.',
                'entry_fees': 'Free',
                'timings': 'Open 24 Hours',
                'is_verified': True,
            },
            {
                'title': 'Bhatye Beach & Coconut Plantations',
                'slug': 'bhatye-beach',
                'category': 'Beach',
                'location_name': 'Bhatye, Ratnagiri (3 km south)',
                'latitude': 16.9680,
                'longitude': 73.2960,
                'description': 'A 1.5 km long flat silver-sand beach fringed with suru (casuarina) trees and coconut palms, opposite the Bhatye Regional Coconut Research Center.',
                'best_time_to_visit': 'Winter & post-monsoon evenings',
                'travel_tips': 'Try fresh tender coconut water and spicy chat stalls along the beachfront promenade.',
                'entry_fees': 'Free',
                'timings': 'Open 24 Hours',
                'is_verified': True,
            },
            {
                'title': 'Aare Ware Twin Beach Coastal Drive',
                'slug': 'aare-ware-beaches',
                'category': 'Beach',
                'location_name': 'Malgund-Ratnagiri Coastal Highway',
                'latitude': 17.0782,
                'longitude': 73.2753,
                'description': 'Two pristine, secluded virgin beaches separated by a scenic cliffside coastal highway, consistently rated among India’s most scenic ocean drives.',
                'best_time_to_visit': 'Golden hour (4:30 PM - 6:30 PM)',
                'travel_tips': 'Stop at the Aare Ware Viewpoint on the cliff for drone-like panoramic photography of the ocean curve.',
                'entry_fees': 'Free',
                'timings': 'Open 24 Hours (Daylight recommended)',
                'is_verified': True,
            },
            {
                'title': 'Swami Swaroopanand Ashram, Pawas',
                'slug': 'pawas-ashram',
                'category': 'Temple',
                'location_name': 'Pawas, Ratnagiri (18 km south)',
                'latitude': 16.8833,
                'longitude': 73.3500,
                'description': 'A serene spiritual sanctuary where Swami Swaroopanand, revered saint and scholar of the Dnyaneshwari, resided for 40 years until his samadhi in 1974.',
                'best_time_to_visit': 'Year-round; early morning meditation',
                'travel_tips': 'Maintain silence in the meditation halls. The ashram offers wholesome satvik Mahaprasad at noon.',
                'entry_fees': 'Free',
                'timings': '06:00 AM - 08:00 PM',
                'is_verified': True,
            },
            {
                'title': 'Lokmanya Bal Gangadhar Tilak Birth Home',
                'slug': 'tilak-smarak',
                'category': 'Viewpoint',
                'location_name': 'Tilak Ali, Ratnagiri City',
                'latitude': 16.9912,
                'longitude': 73.3015,
                'description': 'The ancestral Konkani wada home where freedom fighter Lokmanya Bal Gangadhar Tilak was born in 1856, preserved as a national memorial and heritage museum.',
                'best_time_to_visit': 'Morning or afternoon',
                'travel_tips': 'Admire the classic Konkani teak-wood architectural layout and historical freedom movement archives.',
                'entry_fees': 'Free',
                'timings': '09:00 AM - 01:00 PM, 02:30 PM - 06:00 PM (Closed Mondays)',
                'is_verified': True,
            },
            {
                'title': 'Bhagwati Mandir (Ratnadurg Cliff)',
                'slug': 'bhagwati-mandir-ratnagiri',
                'category': 'Temple',
                'location_name': 'Inside Ratnadurg Fort, Ratnagiri',
                'latitude': 16.9860,
                'longitude': 73.2680,
                'description': 'An ancient temple dedicated to Goddess Bhagwati situated inside the outer perimeter of Ratnadurg Fort, famous for Navratri celebrations.',
                'best_time_to_visit': 'Morning aarti or during Navratri festival',
                'travel_tips': 'Combine with the Ratnadurg fort exploration and cliff walk.',
                'entry_fees': 'Free',
                'timings': '06:00 AM - 07:00 PM',
                'is_verified': True,
            },
        ]

        for dest_data in destinations_data:
            Destination.objects.update_or_create(
                slug=dest_data['slug'],
                defaults=dest_data
            )

        # 1. Emergency Contacts
        contacts_data = [
            {
                'name': 'Ratnagiri District Civil Hospital (24x7)',
                'category': 'HOSPITAL',
                'phone_number': '+91 2352 222333',
                'alternate_phone': '108',
                'address': 'Jail Road, Near District Court, Ratnagiri, Maharashtra 415612',
                'latitude': 16.9934,
                'longitude': 73.3056,
                'is_24x7': True,
                'order': 1,
            },
            {
                'name': 'Ratnagiri City Police Control Room',
                'category': 'POLICE',
                'phone_number': '112',
                'alternate_phone': '+91 2352 222222',
                'address': 'SP Office Complex, Ratnagiri, Maharashtra 415612',
                'latitude': 16.9902,
                'longitude': 73.3120,
                'is_24x7': True,
                'order': 2,
            },
            {
                'name': 'Mirya Coastal & Marine Security Police',
                'category': 'COASTAL_POLICE',
                'phone_number': '+91 2352 232100',
                'address': 'Mirya Port Road, Ratnagiri, Maharashtra',
                'latitude': 17.0210,
                'longitude': 73.2730,
                'is_24x7': True,
                'order': 3,
            },
            {
                'name': 'Emergency Medical Ambulance (Toll-Free)',
                'category': 'AMBULANCE',
                'phone_number': '108',
                'address': 'Dispatched from nearest primary health center',
                'is_24x7': True,
                'order': 4,
            },
            {
                'name': 'Maharashtra Tourism Tourist Helpline',
                'category': 'TOURIST_HELPLINE',
                'phone_number': '1800 229 930',
                'address': 'MTDC Regional Office, Ratnagiri',
                'is_24x7': False,
                'order': 5,
            },
        ]

        for c in contacts_data:
            EmergencyContact.objects.update_or_create(
                name=c['name'],
                defaults=c
            )

        # 2. Sample Partners
        partners_data = [
            {
                'business_name': 'Hotel Sea Breeze & Coastal Suites',
                'slug': 'hotel-sea-breeze',
                'partner_type': 'HOTEL',
                'short_tagline': 'Beachfront retreat overlooking the Arabian Sea in Ratnagiri.',
                'description': 'Premium oceanfront accommodation with complimentary NFC smart room guides, authentic Konkani dining, and sunset terraces.',
                'address': 'Bhatye Beach Road, Ratnagiri, Maharashtra 415612',
                'phone': '+91 98220 12345',
                'whatsapp': '+91 98220 12345',
                'website': 'https://example.com/sea-breeze',
                'latitude': 16.9750,
                'longitude': 73.2920,
                'is_verified': True,
                'is_featured': True,
            },
            {
                'business_name': 'Atithi Parinay Heritage Homestay',
                'slug': 'atithi-parinay-homestay',
                'partner_type': 'HOMESTAY',
                'short_tagline': 'Eco-friendly traditional Konkani courtyard stay.',
                'description': 'Experience traditional red-laterite architecture, farm-fresh Ukadiche Modak, and tranquil coconut groves in Kotawade village.',
                'address': 'Kotawade, Near Ganpatipule, Ratnagiri 415617',
                'phone': '+91 98230 54321',
                'whatsapp': '+91 98230 54321',
                'latitude': 17.0850,
                'longitude': 73.3100,
                'is_verified': True,
                'is_featured': True,
            },
            {
                'business_name': 'Chaitanya Authentic Malvani Kitchen',
                'slug': 'chaitanya-malvani-kitchen',
                'partner_type': 'RESTAURANT',
                'short_tagline': 'Legendary Surmai thalis, Crab masala & Solkadhi.',
                'description': 'Celebrated local dining spot for fresh catch of the day, authentic Kokani home masalas, and refreshing Solkadhi.',
                'address': 'Main Market Road, Near Mandvi Beach, Ratnagiri',
                'phone': '+91 2352 271234',
                'latitude': 16.9880,
                'longitude': 73.2950,
                'is_verified': True,
                'is_featured': True,
            },
            {
                'business_name': 'Nivant Retreat',
                'slug': 'nivant-retreat',
                'partner_type': 'HOMESTAY',
                'short_tagline': 'Cozy Homestay near Ganeshgule | Peaceful, Private & Close to the Sea',
                'description': (
                    "Experience the timeless charm of coastal Maharashtra with a relaxing stay, "
                    "welcoming hospitality, and a serene atmosphere away from the hustle and bustle "
                    "of city life. Whether you're visiting with family, friends, or loved ones, "
                    "Nivant Retreat is an ideal place to unwind, explore nearby beaches and local "
                    "attractions, and enjoy an authentic Konkan experience."
                ),
                'address': 'Near Ganeshgule Beach, Ratnagiri, Maharashtra 415616',
                'phone': '+91 92707 34472',
                'whatsapp': '+91 92707 34472',
                'email': 'nivantretreat@gmail.com',
                'website': 'https://www.instagram.com/nivantretreat/',
                'google_maps_url': 'https://maps.google.com/?q=16.9080,73.2985',
                'latitude': 16.9080,
                'longitude': 73.2985,
                'is_verified': True,
                'is_featured': True,
            }
        ]

        partner_objs = {}
        for p in partners_data:
            obj, _ = Partner.objects.update_or_create(
                slug=p['slug'],
                defaults=p
            )
            partner_objs[p['slug']] = obj

        # 3. Curated Itineraries
        dest_map = {d.title.lower(): d for d in Destination.objects.all()}

        itineraries_data = [
            {
                'title': '2-Day Essential Ratnagiri (Forts, Beaches & Food Trail)',
                'slug': 'ratnagiri-2-day',
                'tagline': 'The quintessential Konkan weekend: Ratnadurg Fort, pristine Bhatye Beach, Thiba Palace, and fresh seafood.',
                'description': 'The ultimate introduction to Ratnagiri. Designed for weekend travelers arriving from Mumbai or Pune, covering monumental sea forts, tranquil beach sunsets, royal history, and authentic Konkani delicacies.',
                'duration_days': 2,
                'audience': 'ALL',
                'season': 'ALL',
                'difficulty': 'EASY',
                'estimated_cost_inr': '₹2,500 - ₹4,500 / person',
                'total_distance_km': 48.0,
                'is_featured': True,
                'order': 1,
                'days': [
                    {
                        'day_number': 1,
                        'title': 'Sea Forts, Royal Legacies & Sunset Horizons',
                        'summary': 'Explore the dramatic walls of Ratnadurg Fort, pay homage at Bhagwati Temple, and watch the crimson sun sink into the Arabian Sea at Bhatye Beach.',
                        'stops': [
                            {
                                'custom_title': 'Ratnadurg Fort & Bhagwati Temple',
                                'stop_type': 'FORT',
                                'order_index': 1,
                                'start_time': '08:30 AM',
                                'duration_minutes': 90,
                                'activity_description': 'Walk along the laterite ramparts surrounded on three sides by the turquoise Arabian Sea. Visit the serene Bhagwati temple inside the fort citadel.',
                                'travel_note_to_next': '10 min scenic drive down to the lighthouse',
                                'travel_time_minutes': 10,
                                'tips': 'Visit early morning to beat the coastal midday sun and catch crisp sea breezes.',
                            },
                            {
                                'custom_title': 'Ratnagiri Lighthouse & Cliff Point',
                                'stop_type': 'SIGHTSEEING',
                                'order_index': 2,
                                'start_time': '10:30 AM',
                                'duration_minutes': 45,
                                'activity_description': 'Panoramic 360-degree viewpoint looking out over Mirya Bay and fishing boats navigating the harbour mouth.',
                                'travel_note_to_next': '15 min drive to town center for lunch',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Authentic Malvani Seafood Lunch (Surmai Thali & Solkadhi)',
                                'stop_type': 'LUNCH',
                                'order_index': 3,
                                'start_time': '12:30 PM',
                                'duration_minutes': 75,
                                'activity_description': 'Feast on freshly fried Surmai or Pomfret, accompanied by warm Ghavane (rice crepes), Tisrya masala (clams), and pink Kokum Solkadhi.',
                                'travel_note_to_next': '10 min drive to Thiba Palace',
                                'travel_time_minutes': 10,
                            },
                            {
                                'custom_title': 'Thiba Palace & Cultural Gardens',
                                'stop_type': 'SIGHTSEEING',
                                'order_index': 4,
                                'start_time': '03:30 PM',
                                'duration_minutes': 60,
                                'activity_description': 'Discover the historic teakwood residence built for King Thibaw of Burma during his British internment. Enjoy the lush garden viewpoints.',
                                'travel_note_to_next': '15 min drive to Bhatye Beach',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Bhatye Beach Walk & Sunset Solkadhi',
                                'stop_type': 'SUNSET',
                                'order_index': 5,
                                'start_time': '05:30 PM',
                                'duration_minutes': 90,
                                'activity_description': 'Stroll along the wide silver-sand beach, sample spicy coastal chaat and hot roasted corn while watching a glowing Konkan sunset.',
                                'travel_note_to_next': 'Return to hotel / resort',
                                'travel_time_minutes': 15,
                            }
                        ]
                    },
                    {
                        'day_number': 2,
                        'title': 'Ganpatipule Coastal Drive & Mango Heritage',
                        'summary': 'Cruise along the world-famous Aare Ware Marine Drive, visit the holy Ganpatipule Temple by the surf, and purchase authentic Alphonso mango products.',
                        'stops': [
                            {
                                'custom_title': 'Aare Ware Marine Coastal Drive',
                                'stop_type': 'ADVENTURE',
                                'order_index': 1,
                                'start_time': '08:30 AM',
                                'duration_minutes': 60,
                                'activity_description': 'One of India’s most scenic coastal roads hugging towering cliffs on one side and endless blue ocean on the other.',
                                'travel_note_to_next': '20 min drive to Ganpatipule',
                                'travel_time_minutes': 20,
                            },
                            {
                                'custom_title': 'Ganpatipule Swayambhu Temple & Beach',
                                'stop_type': 'BEACH',
                                'order_index': 2,
                                'start_time': '10:30 AM',
                                'duration_minutes': 90,
                                'activity_description': 'Offer prayers at the 400-year-old deity resting right on the beach sands, then stroll the clean white-sand shoreline.',
                                'travel_note_to_next': '10 min walk to local lunch kitchen',
                                'travel_time_minutes': 10,
                            },
                            {
                                'custom_title': 'Traditional Konkani Vegetarian Feast (Ukadiche Modak)',
                                'stop_type': 'LUNCH',
                                'order_index': 3,
                                'start_time': '01:00 PM',
                                'duration_minutes': 60,
                                'activity_description': 'Savour steaming hot Ukadiche Modak filled with fresh grated coconut and jaggery, paired with fragrant Amti and rice.',
                                'travel_note_to_next': '15 min drive to local spice & mango market',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Local Mango Products & Cashew Shopping',
                                'stop_type': 'SHOPPING',
                                'order_index': 4,
                                'start_time': '03:30 PM',
                                'duration_minutes': 60,
                                'activity_description': 'Pick up authentic Hapus (Alphonso) pulp, Aam Papad, Phanas poli, and freshly roasted whole Konkan cashews.',
                                'travel_note_to_next': 'Departure / Railway Station',
                                'travel_time_minutes': 30,
                            }
                        ]
                    }
                ]
            },
            {
                'title': '1-Day Express Ratnagiri (Best Highlights in 8 Hours)',
                'slug': 'ratnagiri-1-day',
                'tagline': 'Have only one day? Experience the absolute best forts, food, and ocean views without rushing.',
                'description': 'Tailored specifically for day-trippers and transit travelers looking to maximize their time in Ratnagiri with precision stop timing and optimal driving routes.',
                'duration_days': 1,
                'audience': 'SOLO',
                'season': 'ALL',
                'difficulty': 'MODERATE',
                'estimated_cost_inr': '₹1,200 - ₹2,500 / person',
                'total_distance_km': 28.0,
                'is_featured': True,
                'order': 2,
                'days': [
                    {
                        'day_number': 1,
                        'title': 'Ratnagiri in 8 Hours',
                        'summary': 'From cliffside ramparts to coastal cuisine and sunset sands.',
                        'stops': [
                            {
                                'custom_title': 'Morning at Ratnadurg Fort',
                                'stop_type': 'FORT',
                                'order_index': 1,
                                'start_time': '09:00 AM',
                                'duration_minutes': 90,
                                'activity_description': 'Explore historic sea ramparts and the lighthouse vantage.',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Coastal Fish Thali Lunch',
                                'stop_type': 'LUNCH',
                                'order_index': 2,
                                'start_time': '12:30 PM',
                                'duration_minutes': 60,
                                'activity_description': 'Fresh pomfret / surmai fry and solkadhi in town.',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Thiba Palace & Heritage Walk',
                                'stop_type': 'SIGHTSEEING',
                                'order_index': 3,
                                'start_time': '02:30 PM',
                                'duration_minutes': 60,
                                'activity_description': 'Royal Burmese exile mansion & panoramic hillside view.',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Sunset at Mandvi Black Sand Beach',
                                'stop_type': 'SUNSET',
                                'order_index': 4,
                                'start_time': '05:00 PM',
                                'duration_minutes': 90,
                                'activity_description': 'Unique black sands and bustling evening street food stalls.',
                                'travel_time_minutes': 20,
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Family Holiday Trail (Safe Waters, Temples & Nature)',
                'slug': 'family-konkan-holiday',
                'tagline': 'Child-friendly beaches, gentle waters, rich cultural temples, and comfortable transit.',
                'description': 'A relaxed itinerary created for families with children and elders. Features accessible paved paths, safe swim zones, clean amenities, and wholesome dining.',
                'duration_days': 2,
                'audience': 'FAMILY',
                'season': 'WINTER',
                'difficulty': 'EASY',
                'estimated_cost_inr': '₹3,000 - ₹5,000 / day',
                'total_distance_km': 42.0,
                'is_featured': True,
                'order': 3,
                'days': [
                    {
                        'day_number': 1,
                        'title': 'Gentle Waters & Heritage Gardens',
                        'summary': 'Calm shores and relaxed palace gardens suited for all ages.',
                        'stops': [
                            {
                                'custom_title': 'Bhatye Beach Family Sandcastle & Walk',
                                'stop_type': 'BEACH',
                                'order_index': 1,
                                'start_time': '09:00 AM',
                                'duration_minutes': 90,
                                'activity_description': 'Flat, wide, safe beach shoreline for children to play.',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Thiba Palace Heritage Stroll & Picnic Lawn',
                                'stop_type': 'SIGHTSEEING',
                                'order_index': 2,
                                'start_time': '11:30 AM',
                                'duration_minutes': 60,
                                'activity_description': 'Shaded lawns and museum exhibits.',
                                'travel_time_minutes': 15,
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Couples & Romantic Sunset Trail',
                'slug': 'romantic-sunset-trail',
                'tagline': 'Cliffside sea lookouts, secluded cove walks, and quiet candlelight coastal dining.',
                'description': 'Designed for couples seeking scenic photography spots, serene horizons, and quiet moments across the Konkan coastline.',
                'duration_days': 2,
                'audience': 'COUPLE',
                'season': 'WINTER',
                'difficulty': 'EASY',
                'estimated_cost_inr': '₹3,500 - ₹6,000 / day',
                'total_distance_km': 55.0,
                'is_featured': True,
                'order': 4,
                'days': [
                    {
                        'day_number': 1,
                        'title': 'Aare Ware Clifftops & Candlelight',
                        'summary': 'Dramatic clifftop vistas over the crashing Arabian Sea waves.',
                        'stops': [
                            {
                                'custom_title': 'Aare Ware Ocean Overlook Point',
                                'stop_type': 'SUNSET',
                                'order_index': 1,
                                'start_time': '04:30 PM',
                                'duration_minutes': 90,
                                'activity_description': 'Unrivaled sunset colors casting gold across the marine bypass cliffs.',
                                'travel_time_minutes': 20,
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Taste of Ratnagiri Culinary & Mango Trail',
                'slug': 'taste-of-ratnagiri',
                'tagline': 'Malvani seafood masalas, Ukadiche Modak, Ghavane, Solkadhi, and world-renowned Alphonso mangoes.',
                'description': 'A food-lover’s expedition through bustling morning fish docks, family spice mills, authentic home thali joints, and heritage sweet shops.',
                'duration_days': 1,
                'audience': 'FOODIE',
                'season': 'ALL',
                'difficulty': 'EASY',
                'estimated_cost_inr': '₹1,500 - ₹3,000 / person',
                'total_distance_km': 25.0,
                'is_featured': True,
                'order': 5,
                'days': [
                    {
                        'day_number': 1,
                        'title': 'From Morning Ghavane to Evening Surmai',
                        'summary': 'The ultimate Konkan culinary marathon.',
                        'stops': [
                            {
                                'custom_title': 'Breakfast: Hot Ghavane & Coconut Chutney with Chaha',
                                'stop_type': 'BREAKFAST',
                                'order_index': 1,
                                'start_time': '08:30 AM',
                                'duration_minutes': 45,
                                'activity_description': 'Light, lacy rice-flour pancakes served with sweetened coconut milk.',
                                'travel_time_minutes': 10,
                            },
                            {
                                'custom_title': 'Mirya Harbour Morning Fish Auction Walk',
                                'stop_type': 'MORNING',
                                'order_index': 2,
                                'start_time': '09:45 AM',
                                'duration_minutes': 45,
                                'activity_description': 'Witness colourful trawlers bringing in kingfish, prawns, and crabs.',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Lunch: Surmai & Prawns Malvani Thali',
                                'stop_type': 'LUNCH',
                                'order_index': 3,
                                'start_time': '01:00 PM',
                                'duration_minutes': 75,
                                'activity_description': 'Spiced fried fish, seafood curry, rice, and double solkadhi.',
                                'travel_time_minutes': 15,
                            },
                            {
                                'custom_title': 'Dessert & Souvenirs: Mango Pulp & Cashew Tasting',
                                'stop_type': 'SHOPPING',
                                'order_index': 4,
                                'start_time': '04:00 PM',
                                'duration_minutes': 60,
                                'activity_description': 'Sample dried mango poli, cashew feni vinegar, and fresh modaks.',
                                'travel_time_minutes': 15,
                            }
                        ]
                    }
                ]
            }
        ]

        for itin_data in itineraries_data:
            days_data = itin_data.pop('days', [])
            itin_obj, _ = Itinerary.objects.update_or_create(
                slug=itin_data['slug'],
                defaults=itin_data
            )
            for d_data in days_data:
                stops_data = d_data.pop('stops', [])
                day_obj, _ = ItineraryDay.objects.update_or_create(
                    itinerary=itin_obj,
                    day_number=d_data['day_number'],
                    defaults=d_data
                )
                for s_data in stops_data:
                    ItineraryStop.objects.update_or_create(
                        day=day_obj,
                        order_index=s_data['order_index'],
                        defaults=s_data
                    )

        # 4. Sample Smart NFC Tags
        tags_data = [
            {
                'tag_uid': 'RATNA-HOTEL-01',
                'title': 'Hotel Sea Breeze - Guest Room NFC Tag',
                'tag_type': 'HOTEL',
                'target_experience': 'HOME',
                'assigned_partner': partner_objs.get('hotel-sea-breeze'),
                'custom_welcome_title': 'Welcome Guest of Hotel Sea Breeze 🌴',
                'custom_welcome_message': 'Your personal digital concierge is ready with curated itineraries, beach guides, and emergency help.',
                'tap_count': 142,
                'unique_visitor_count': 98,
            },
            {
                'tag_uid': 'RATNA-2DAY-TRIP',
                'title': '2-Day Essential Ratnagiri Itinerary Tag',
                'tag_type': 'ITINERARY',
                'target_experience': 'SPECIFIC_ITINERARY',
                'assigned_itinerary': Itinerary.objects.filter(slug='ratnagiri-2-day').first(),
                'custom_welcome_title': 'Your 2-Day Ratnagiri Journey Starts Now!',
                'custom_welcome_message': 'Follow this curated step-by-step route with live directions and dining stops.',
                'tap_count': 324,
                'unique_visitor_count': 215,
            },
            {
                'tag_uid': 'RATNA-FOOD-TRAIL',
                'title': 'Taste of Ratnagiri Food Trail Tag',
                'tag_type': 'FOOD_TRAIL',
                'target_experience': 'FOOD_TRAIL',
                'custom_welcome_title': 'Taste the Flavours of Ratnagiri 🍛',
                'custom_welcome_message': 'Discover authentic seafood, sweet mango specialties, and secret local food joints.',
                'tap_count': 89,
                'unique_visitor_count': 74,
            },
            {
                'tag_uid': 'RATNA-SOS-SAFETY',
                'title': 'Tourist SOS Emergency Assistance Tag',
                'tag_type': 'EMERGENCY',
                'target_experience': 'EMERGENCY',
                'custom_welcome_title': '1-Click Tourist Emergency & Safety Center 🚨',
                'custom_welcome_message': 'Instant telephone links to 24x7 hospitals, police control, coastal rescue, and tourist helpline.',
                'tap_count': 31,
                'unique_visitor_count': 29,
            },
            {
                'tag_uid': 'RATNA-NEAR-ME',
                'title': 'Live Radar "What\'s Near Me" Tag',
                'tag_type': 'GENERAL',
                'target_experience': 'NEAR_ME',
                'custom_welcome_title': 'Live Tourist Radar 📍',
                'custom_welcome_message': 'Detecting closest beaches, sea forts, restaurants, and fuel pumps around you.',
                'tap_count': 210,
                'unique_visitor_count': 160,
            },
            {
                'tag_uid': 'RATNA-NIVANT-01',
                'title': 'Nivant Retreat - Guest Room NFC Concierge',
                'tag_type': 'HOTEL',
                'target_experience': 'PARTNER_PAGE',
                'assigned_partner': partner_objs.get('nivant-retreat'),
                'custom_welcome_title': 'Welcome to Nivant Retreat 🌴',
                'custom_welcome_message': 'Your peaceful coastal staycation in Ratnagiri. Beach is just 4 km away! Tap here for curated Konkan itineraries, food spots, and instant concierge assistance.',
                'tap_count': 56,
                'unique_visitor_count': 42,
            }
        ]

        for t in tags_data:
            NFCTag.objects.update_or_create(
                tag_uid=t['tag_uid'],
                defaults=t
            )

        # 5. FAQs
        faqs_data = [
            {
                'question': 'When is the best season to visit Ratnagiri for authentic Alphonso Mangoes?',
                'answer': 'The Ratnagiri Hapus (Alphonso) mango season peaks from late March through May. During this time, local mango orchards in Pawas, Malgund, and Devgad offer direct farm tours, fresh tastings, and authentic GI-tagged mango boxes.',
                'category': 'FOOD',
                'order': 1,
                'is_published': True,
            },
            {
                'question': 'How does the physical NFC smart tag work?',
                'answer': 'Simply hold your NFC-enabled smartphone near the tag (room table, reception, or beach sign). It opens the digital companion web app instantly with zero app download or registration required.',
                'category': 'NFC',
                'order': 2,
                'is_published': True,
            },
            {
                'question': 'Is sea swimming safe along Ratnagiri beaches?',
                'answer': 'During winter and summer (October to May), beaches like Ganpatipule, Bhatye, and Mandvi are generally calm for wading. However, swimming during monsoon (June to September) or high tide is strictly prohibited due to dangerous rip currents.',
                'category': 'SAFETY',
                'order': 3,
                'is_published': True,
            },
            {
                'question': 'How can I travel locally between Ratnagiri town and Ganpatipule?',
                'answer': 'MSRTC state transport buses depart every 30 minutes from Ratnagiri Central Bus Stand to Ganpatipule (₹35-₹50). Private taxis and auto-rickshaws are available at Ratnagiri railway station (approx. ₹600-₹900 one way).',
                'category': 'TRANSPORT',
                'order': 4,
                'is_published': True,
            },
        ]
        for f in faqs_data:
            FAQ.objects.update_or_create(question=f['question'], defaults=f)

        # 6. Travel Tips
        tips_data = [
            {
                'title': 'Best Golden Hour Photography Spots',
                'content': 'Reach Ratnadurg Fort outer bastion or the Aare Ware coastal cliff viewpoint between 5:15 PM and 6:30 PM for breathtaking Arabian Sea sunset photography.',
                'category': 'PHOTO',
                'icon': 'fa-camera',
                'is_active': True,
                'order': 1,
            },
            {
                'title': 'Digestive Secret: Authentic Solkadhi',
                'content': 'After enjoying spicy Malvani fish or mutton thalis, sip freshly made Solkadhi (steeped kokum, coconut milk, garlic, and green chilies) — the traditional Konkani digestive cooling drink.',
                'category': 'CULTURE',
                'icon': 'fa-utensils',
                'is_active': True,
                'order': 2,
            },
            {
                'title': 'Tide Awareness & Footwear',
                'content': 'When exploring historic sea forts like Ratnadurg and Jaigad, wear grippy rubber-soled shoes for wet laterite rock surfaces and check daily tide times.',
                'category': 'PACKING',
                'icon': 'fa-shoe-prints',
                'is_active': True,
                'order': 3,
            },
        ]
        for tip in tips_data:
            TravelTip.objects.update_or_create(title=tip['title'], defaults=tip)

        # 7. Announcements
        Announcement.objects.update_or_create(
            title='Ratnagiri Coastal & Hapus Mango Season 2026',
            defaults={
                'message': 'Direct orchard farm tours and GI-tagged mango tastings are now live across Pawas and Malgund coastal belts. Check the Food Trail for top orchard stops.',
                'urgency_level': 'INFO',
                'link_url': '/food-trail/',
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Ratnagiri NFC Tourist Companion data & CMS content!"))
