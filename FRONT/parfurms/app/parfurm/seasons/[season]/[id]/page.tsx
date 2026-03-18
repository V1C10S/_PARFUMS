import Link from "next/link";
import { Quicksand } from "next/font/google";
import { notFound } from "next/navigation";
import Image from "next/image";

const quicksand = Quicksand({ subsets: ["latin"] });

type Perfume = {
  name: string;
  brand: string;
  season: string;
  main_image: string;
  price: number;
  currency: string;
  volume: string;
  rating: string;
  performance: {
    projection: number;
    longevity: number;
    day_use: number;
    night_use: number;
  };
  description: string;
  accords: string[];
  notes: {
    top: string[];
    middle: string[];
    base: string[];
  };
};

type IDpage = { params: {season: string; id: string;}; };

const validSeasons = ["spring", "summer", "fall", "winter"] as const;

function formatSeasonTitle(season: string) {
  const titles: Record<string, string> = {
    spring: "Spring",
    summer: "Summer",
    fall: "Fall",
    winter: "Winter",
  };

  return titles[season] ?? season;
}

function capitalizeWords(text: string) {
  return text
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export default async function IDpage({ params }: IDpage) {
  
  const { season, id } = await params;

  if (!validSeasons.includes(season as (typeof validSeasons)[number])) {
    notFound();
  }

  const response = await fetch(`http://localhost:5500/parfurm/seasons/${season}/${id}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.log("FETCH STATUS:", response.status);
    console.log("FETCH BODY:", errorText);
    throw new Error(`Erro ao buscar o perfume da estação ${season}. Status: ${response.status}`);
  }

  const perfume:Perfume = await response.json();

  return (

    <main className="min-h-screen bg-gradient-to-b from-neutral-50 to-neutral-400">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-14 text-center">
          <Link href={`/parfurm`}>
            <h1 className={`${quicksand.className} text-6xl font-light tracking-widest text-neutral-800`}>
              L’ÉLU PARFUMS
            </h1>
          </Link>
            <h2 className={`${quicksand.className} mt-8 text-2xl font-light tracking-wide text-neutral-600`}>L’art de choisir son parfum idéal</h2>
        </header>



        <section className="mx-auto w-5xl">

          <div className="flex flex items-start">
            <div className="relative aspect-[3/4] w-full">

              <Image
                src={perfume.main_image}
                alt={perfume.name}
                fill
                className="object-contain p-40"
                sizes="(max-width: 1024px) 100vw, 330px"
              />

            </div>

            <div className="mt-100 pl-20">

              <p className={`${quicksand.className} text-4xl tracking-wide text-neutral-700`}>
                {capitalizeWords(perfume.brand)}</p>

              <p className={`${quicksand.className} mt-6 text-4xl tracking-wide text-neutral-700`}>
                {capitalizeWords(perfume.name)}</p>
            </div>
          </div>

        </section>

      </div>
    </main>
  );
}