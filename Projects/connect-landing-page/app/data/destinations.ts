// Proposal 1: Scalability-First Architecture
// Simulating Server-Side Data Fetching Structure

export interface Destination {
  id: string;
  city: string;
  country: string;
  flag: string; // Emoji flag for simplicity in mock
  description: string;
}

export const destinations: Destination[] = [
  {
    id: '1',
    city: 'Тель-Авив',
    country: 'Израиль',
    flag: '🇮🇱',
    description: 'Город, который никогда не спит. Пляжи, технологии и ночная жизнь.',
  },
  {
    id: '2',
    city: 'Нью-Йорк',
    country: 'США',
    flag: '🇺🇸',
    description: 'Бетонные джунгли, где рождаются мечты.',
  },
  {
    id: '3',
    city: 'Лондон',
    country: 'Великобритания',
    flag: '🇬🇧',
    description: 'История встречается с современностью в сердце Британии.',
  },
  {
    id: '4',
    city: 'Токио',
    country: 'Япония',
    flag: '🇯🇵',
    description: 'Неоновый микс традиций и технологий будущего.',
  },
  {
    id: '5',
    city: 'Париж',
    country: 'Франция',
    flag: '🇫🇷',
    description: 'Город огней, любви и круассанов.',
  },
];

export async function getDestinations(): Promise<Destination[]> {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 200));
  return destinations;
}
