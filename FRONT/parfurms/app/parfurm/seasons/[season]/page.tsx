import Link from "next/link";
import { Quicksand } from "next/font/google";
import { notFound } from "next/navigation";
import Image from "next/image";

const quicksand = Quicksand({ subsets: ["latin"] });

type Perfume = {
  id: string;
  name: string;
  brand: string;
  main_image: string;
};

type SeasonPageProps = {
  params: {
    season: string;
  };
};

const seasons = ["spring", "summer", "fall", "winter"] as const;

function capitalizeWords(text: string) {
  return text
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export default async function Season({ params }: SeasonPageProps) {
  const { season } = await params;

  if (!seasons.includes(season as (typeof seasons)[number])) {
    notFound();
  }

  const response = await fetch(
    `http://localhost:5500/parfurm/seasons/${season}`,
    { cache: "no-store" }
  );

  if (!response.ok) {
    const errorText = await response.text();
    console.log("FETCH STATUS:", response.status);
    console.log("FETCH BODY:", errorText);
    throw new Error(`Erro ao buscar os perfumes da estação. Status: ${response.status}`);
  }

  const perfumes: Perfume[] = await response.json();

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

        <section className="mx-auto max-w-7xl">
          
          <div className="grid grid-cols-3  gap-6">
            {perfumes.map((perfume) => (
              
              <Link
                key={perfume.id}
                href={`/parfurm/seasons/${season}/${perfume.id}`}
                className="w-[330px] rounded-2xl bg-black/15 p-4 transition hover:bg-black/15">

                <div className="relative aspect-[3/4] overflow-hidden rounded-xl bg-neutral-200/20">
          
                  <Image
                    src={perfume.main_image}
                    alt={perfume.name}
                    fill
                    className="object-contain p-3"
                    sizes="w-[1020px] 100vw, 330px"
                  />

                </div>    

                <div className="mt-4 w-4/4 rounded-xl bg-neutral-200/60 px-3 py-2">
                  <p className={`${quicksand.className} text-sm text-neutral-800`}>
                    {capitalizeWords(perfume.name)}  {capitalizeWords(perfume.brand)}
                  </p>
                </div>
              </Link>

            ))}
          </div>

        </section>

      </div>
    </main>
  );
}