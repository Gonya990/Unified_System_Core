import { TOP_COUNTRIES } from "@/app/data/countries"
import ConnectivityHub from "@/app/components/ConnectivityHub"
import { Metadata } from "next"

interface Props {
    params: Promise<{ slug: string }>
}

export async function generateStaticParams() {
    return TOP_COUNTRIES.map((country) => ({
        slug: country.slug,
    }))
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const { slug } = await params
    const country = TOP_COUNTRIES.find((c) => c.slug === slug)

    if (!country) {
        return {
            title: "Country Not Found - Connect Global",
        }
    }

    return {
        title: `eSIM in ${country.name} - Connect Globally`,
        description: `Stay connected in ${country.name} with premium eSIM plans. High-speed 5G data, instant activation, and local coverage in ${country.region}.`,
        keywords: `eSIM ${country.name}, mobile data ${country.name}, travel sim ${country.name}, Connect Global`,
    }
}

export default async function CountryPage({ params }: Props) {
    const { slug } = await params
    const country = TOP_COUNTRIES.find((c) => c.slug === slug)

    if (!country) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-[#111418] text-white">
                <h1 className="text-2xl font-bold">Country not found</h1>
            </div>
        )
    }

    // Passing the formatted string exactly as the UI expects it
    const initialCountry = `${country.flag} ${country.name}`

    return <ConnectivityHub key={slug} initialCountry={initialCountry} />
}

