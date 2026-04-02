import React from 'react';
import {
  Image,
  Linking,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

const products = [
  {
    id: '1',
    title: 'Sensor de posición del cigüeñal Nissan',
    price: 210.36,
    margin: 49.74,
    decision: 'MEDIA',
    image: 'https://via.placeholder.com/220x220.png?text=PNG',
    link: 'https://www.aliexpress.com/',
  },
  {
    id: '2',
    title: 'Probador de relé automotriz 12V',
    price: 136.59,
    margin: 55.65,
    decision: 'MEDIA',
    image: 'https://via.placeholder.com/220x220.png?text=PNG',
    link: 'https://www.aliexpress.com/',
  },
  {
    id: '3',
    title: 'Audífonos KZ EDX PRO IEM cableados',
    price: 86.59,
    margin: 70.05,
    decision: 'OPORTUNIDAD',
    image: 'https://via.placeholder.com/220x220.png?text=PNG',
    link: 'https://www.aliexpress.com/',
  },
];

const getBadgeStyle = (decision: string) => {
  if (decision === 'OPORTUNIDAD') {
    return {
      backgroundColor: '#d1fae5',
      color: '#065f46',
    };
  }

  if (decision === 'MEDIA') {
    return {
      backgroundColor: '#fef3c7',
      color: '#92400e',
    };
  }

  return {
    backgroundColor: '#e5e7eb',
    color: '#374151',
  };
};

export default function HomeScreen() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      {products.map((product) => (
        <Pressable
          key={product.id}
          style={styles.card}
          onPress={() => Linking.openURL(product.link)}
        >
          <View style={styles.imageWrap}>
            <Image
              source={{ uri: product.image }}
              style={styles.image}
              resizeMode="contain"
            />
          </View>

          <View style={styles.info}>
            <View
              style={[
                styles.badge,
                { backgroundColor: getBadgeStyle(product.decision).backgroundColor },
              ]}
            >
              <Text
                style={[
                  styles.badgeText,
                  { color: getBadgeStyle(product.decision).color },
                ]}
              >
                {product.decision}
              </Text>
            </View>

            <Text style={styles.title} numberOfLines={2}>
              {product.title}
            </Text>

            <Text style={styles.text}>
              Precio: <Text style={styles.value}>${product.price.toFixed(2)} MXN</Text>
            </Text>

            <Text style={styles.text}>
              Margen: <Text style={styles.value}>{product.margin.toFixed(2)}%</Text>
            </Text>
          </View>
        </Pressable>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  content: {
    padding: 18,
    paddingTop: 24,
    alignItems: 'center',
    gap: 18,
  },
  card: {
    width: 260,
    backgroundColor: '#ffffff',
    borderRadius: 24,
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.08)',
    padding: 16,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
    elevation: 3,
  },
  imageWrap: {
    width: '100%',
    height: 220,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.06)',
    backgroundColor: '#fafafa',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
    marginBottom: 14,
  },
  image: {
    width: '88%',
    height: '88%',
  },
  info: {
    gap: 6,
  },
  badge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
    marginBottom: 6,
  },
  badgeText: {
    fontSize: 12,
    fontWeight: '700',
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
    color: '#111111',
    marginBottom: 4,
  },
  text: {
    fontSize: 16,
    color: '#222222',
  },
  value: {
    fontWeight: '700',
    color: '#000000',
  },
});