export const popularDestinations = [
  { country: "United States", flag: "🇺🇸", cities: ["New York", "Los Angeles", "Chicago", "Miami"] },
  { country: "United Kingdom", flag: "🇬🇧", cities: ["London", "Manchester", "Edinburgh", "Birmingham"] },
  { country: "Canada", flag: "🇨🇦", cities: ["Toronto", "Vancouver", "Montreal", "Calgary"] },
  { country: "Australia", flag: "🇦🇺", cities: ["Sydney", "Melbourne", "Brisbane", "Perth"] },
  { country: "Germany", flag: "🇩🇪", cities: ["Berlin", "Munich", "Hamburg", "Frankfurt"] },
  { country: "France", flag: "🇫🇷", cities: ["Paris", "Lyon", "Marseille", "Nice"] },
  { country: "Japan", flag: "🇯🇵", cities: ["Tokyo", "Osaka", "Kyoto", "Yokohama"] },
  { country: "Spain", flag: "🇪🇸", cities: ["Madrid", "Barcelona", "Valencia", "Seville"] },
  { country: "Italy", flag: "🇮🇹", cities: ["Rome", "Milan", "Venice", "Florence"] },
  { country: "Brazil", flag: "🇧🇷", cities: ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"] },
  { country: "Mexico", flag: "🇲🇽", cities: ["Mexico City", "Guadalajara", "Monterrey", "Cancún"] },
  { country: "India", flag: "🇮🇳", cities: ["Mumbai", "Delhi", "Bangalore", "Chennai"] },
]

export type Destination = (typeof popularDestinations)[0]
