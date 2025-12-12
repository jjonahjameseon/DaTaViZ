import requests
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_realistic_data():
    """Génère des données simulées réalistes pour les opérateurs télécoms algériens"""
    companies = ['Ooredoo', 'Djezzy', 'Mobilis']

    # Posts réalistes
    post_contents = [
        "🌐 Nouvelle offre 4G+ avec 50% de data en plus! Profitez-en maintenant!",
        "🔧 Maintenance réseau prévue cette nuit de 00h à 04h. Désolés pour la gêne occasionnée.",
        "📞 Bonjour! Notre service client est disponible 24h/24 pour vous aider.",
        "🎉 Offre spéciale Ramadan! Bénéficiez de forfaits exceptionnels!",
        "⚠️ Attention! Des arnaqueurs se font passer pour nos agents. Ne communiquez jamais vos codes!",
        "📶 Amélioration du réseau dans la région d'Alger. Vos retours sont les bienvenus!",
        "💡 Astuce: Activez la Wi-Fi Calling pour des appels plus clairs!",
        "🎁 Gagnez des forfaits gratuits en participant à notre concours!",
        "🔔 Mise à jour: Résolution des problèmes de connexion signalés hier.",
        "📲 Téléchargez notre nouvelle application My Ooredoo/Djezzy/Mobilis!"
    ]

    # Commentaires réalistes
    positive_comments = [
        "Excellent service! Réseau stable et débit correct 👍",
        "Je suis satisfait de la qualité du service, bon travail!",
        "Service client très professionnel, problème résolu en 10min",
        "ممتاز! الخدمة جيدة والشبكة مستقرة",
        "شكرا على التحسينات في الشبكة",
        "Les nouvelles offres sont intéressantes, bon rapport qualité-prix"
    ]

    negative_comments = [
        "Réseau très lent depuis 3 jours, inacceptable pour le prix payé!",
        "Service client injoignable, j'attends depuis 30 minutes 😠",
        "Facturation excessive, on me facture des services non souscrits",
        "الإنترنت بطيء جدا، لا استطيع العمل",
        "خدمة العملاء سيئة، لا يردون على الهاتف",
        "Pas de signal dans mon immeuble, quand est-ce que ça va être réparé?"
    ]

    neutral_comments = [
        "Quelles sont les zones couvertes par la 4G+ dans la wilaya de Blida?",
        "Comment souscrire à l'offre Ramadan?",
        "ما هي أوقات خدمة العملاء؟",
        "كيف أشترك في العرض الجديد؟",
        "Est-ce que les anciens clients peuvent bénéficier des nouvelles promotions?"
    ]

    # Génération des posts
    posts_data = []
    for i in range(1, 101):
        company = random.choice(companies)
        post_content = random.choice(post_contents)

        # Adapter le contenu selon l'opérateur
        if company == 'Ooredoo':
            post_content = post_content.replace('My Ooredoo/Djezzy/Mobilis', 'My Ooredoo')
        elif company == 'Djezzy':
            post_content = post_content.replace('My Ooredoo/Djezzy/Mobilis', 'My Djezzy')
        else:
            post_content = post_content.replace('My Ooredoo/Djezzy/Mobilis', 'My Mobilis')

        post = {
            'ID': f'POST_{company[0]}_{i:03d}',
            'Contents': post_content,
            'Lien_Post': f'https://facebook.com/{company.lower()}algerie/posts/{i}',
            'Reactions_Like': random.randint(100, 2000),
            'Reactions_Love': random.randint(50, 500),
            'Reactions_Care': random.randint(20, 200),
            'Reactions_Wow': random.randint(30, 400),
            'Reactions_Sad': random.randint(10, 150),
            'Reactions_Angry': random.randint(5, 100),
            'Reactions_Haha': random.randint(40, 300),
            'Company': company,
            'Date': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d %H:%M:%S')
        }
        posts_data.append(post)

    # Génération des commentaires
    comments_data = []
    for post in posts_data:
        num_comments = random.randint(5, 25)

        for j in range(num_comments):
            # Distribution réaliste des sentiments
            sentiment = random.choices(
                ['Positif', 'Négatif', 'Neutre'],
                weights=[0.30, 0.45, 0.25]
            )[0]

            # Sélection du commentaire selon le sentiment
            if sentiment == 'Positif':
                comment_text = random.choice(positive_comments)
            elif sentiment == 'Négatif':
                comment_text = random.choice(negative_comments)
            else:
                comment_text = random.choice(neutral_comments)

            comment = {
                'ID_Post': post['ID'],
                'User_Name': f'User_{random.randint(1000, 9999)}',
                'Comments': comment_text,
                'Sentiments': sentiment,
                'Date_Comment': (datetime.strptime(post['Date'], '%Y-%m-%d %H:%M:%S') +
                               timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S')
            }
            comments_data.append(comment)

    return pd.DataFrame(posts_data), pd.DataFrame(comments_data)

def get_facebook_pages_data(access_token, page_ids):
    """
    Récupère les données via l'API Facebook officielle
    Nécessite un token d'accès approuvé
    """
    base_url = "https://graph.facebook.com/v19.0/"

    all_posts_data = []
    all_comments_data = []

    for page_id in page_ids:
        print(f"Récupération des données pour {page_id}...")

        # Récupérer les posts de la page
        url = f"{base_url}{page_id}/posts"
        params = {
            'access_token': access_token,
            'fields': 'id,message,created_time,likes.summary(true),comments.summary(true),shares',
            'limit': 100
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', [])

                for post in posts:
                    # Données du post
                    post_data = {
                        'ID': post.get('id', ''),
                        'Contents': post.get('message', ''),
                        'Lien_Post': f"https://facebook.com/{post.get('id', '').replace('_', '/posts/')}",
                        'Reactions_Like': post.get('likes', {}).get('summary', {}).get('total_count', 0),
                        'Company': get_company_name(page_id),
                        'Date': post.get('created_time', '')
                    }
                    all_posts_data.append(post_data)

                    # Récupérer les commentaires du post
                    comments_url = f"{base_url}{post['id']}/comments"
                    comments_params = {
                        'access_token': access_token,
                        'fields': 'id,message,from,created_time',
                        'limit': 100
                    }

                    try:
                        comments_response = requests.get(comments_url, params=comments_params)
                        if comments_response.status_code == 200:
                            comments_data = comments_response.json().get('data', [])

                            for comment in comments_data:
                                comment_data = {
                                    'ID_Post': post.get('id', ''),
                                    'User_Name': comment.get('from', {}).get('name', ''),
                                    'Comments': comment.get('message', ''),
                                    'Date_Comment': comment.get('created_time', ''),
                                    'Sentiments': 'Neutre'  # À classifier plus tard
                                }
                                all_comments_data.append(comment_data)

                        time.sleep(1)  # Respect rate limits

                    except Exception as e:
                        print(f"Erreur commentaires pour {post.get('id')}: {e}")

            else:
                print(f" Erreur API pour {page_id}: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Erreur générale pour {page_id}: {e}")

        time.sleep(2)  # Pause entre les pages

    return all_posts_data, all_comments_data

def get_company_name(page_id):
    """Retourne le nom de l'entreprise basé sur l'ID de la page"""
    mapping = {
        'ooredoo.algerie': 'Ooredoo',
        'DjezzyOfficial': 'Djezzy',
        'Mobilis.Algerie': 'Mobilis'
    }
    return mapping.get(page_id, page_id)

def classify_sentiment(comment_text):
    """
    Classification basique des sentiments
    """
    if not isinstance(comment_text, str):
        return 'Neutre'

    text_lower = comment_text.lower()

    positive_words = ['bon', 'excellent', 'super', 'génial', 'bravo', 'merci', 'parfait', 'satisfait', 'bon travail', 'ممتاز', 'شكرا']
    negative_words = ['mauvais', 'nul', 'horrible', 'problème', 'erreur', 'bug', 'lent', 'cher', 'arnaque', 'بطيء', 'سيئة']

    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        return 'Positif'
    elif negative_count > positive_count:
        return 'Négatif'
    else:
        return 'Neutre'

# Configuration
page_ids = ['ooredoo.algerie', 'DjezzyOfficial', 'Mobilis.Algerie']
access_token = "EAAQgB8KhXtkBQIrm89OZCPH9ZAkmCUtm77jJ4bJhTUFQHBCZB8694ZALNX2NKoZAKxTDnbiHhSZCdDuYZC9AZBZBR1AMA5MHyER8hSBFqX61ZCxylosbl4o4A0uoI93UHs8PZCj3tcWAiDTDgxirFi6s3SOXAb2wzjzUoKmWNpLzkyOFZBUaDbs3ZCkLgP4ZBIFdZAXii4w8AZDZD"
USE_SIMULATED_DATA = True

# Programme principal
print(" Démarrage de la génération des datasets...")

if not USE_SIMULATED_DATA and access_token != "VOTRE_TOKEN_ICI":
    print(" Tentative de connexion à l'API Facebook...")
    posts_data, comments_data = get_facebook_pages_data(access_token, page_ids)

    # Sauvegarder les données réelles
    posts_df = pd.DataFrame(posts_data)
    comments_df = pd.DataFrame(comments_data)

else:
    print(" Utilisation des données simulées réalistes...")
    posts_df, comments_df = generate_realistic_data()

# Classifier les sentiments des commentaires
if not comments_df.empty:
    comments_df['Sentiments'] = comments_df['Comments'].apply(classify_sentiment)

# Sauvegarder les fichiers CSV
posts_df.to_csv('posts.csv', index=False, encoding='utf-8-sig')
comments_df.to_csv('comments.csv', index=False, encoding='utf-8-sig')

print("Fichiers CSV créés avec succès!")
print(f" Posts dataset: {len(posts_df)} enregistrements")
print(f"Comments dataset: {len(comments_df)} enregistrements")

# Afficher les statistiques
if not comments_df.empty:
    print("\n📈 Répartition des sentiments:")
    sentiment_counts = comments_df['Sentiments'].value_counts()
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(comments_df)) * 100
        print(f"   {sentiment}: {count} commentaires ({percentage:.1f}%)")

print(f"\n Fichiers générés:")
print("   - facebook_posts_dataset.csv")
print("   - facebook_comments_dataset.csv")
