import Link from "next/link";
import Image from "next/image";
import { Quicksand } from "next/font/google";

const quicksand = Quicksand({
  subsets: ["latin"],
});

const seasons = [
  {
    name: "Spring",
    slug: "spring",
    icon: "/icons/spring.png",
    label: "SPRING",
    imageClass: "opacity-25",
    textClass: "group-hover:text-rose-400",
    hoverScale: "group-hover:scale-125",
  },

  {
    name: "Summer",
    slug: "summer",
    icon: "/icons/summer.png",
    label: "SUMMER",
    imageClass: "opacity-100",
    textClass: "group-hover:text-yellow-400",
    hoverScale: "group-hover:scale-125",
  },

  {
    name: "Fall",
    slug: "fall",
    icon: "/icons/fall.png",
    label: "FALL",
    imageClass: "opacity-35",
    textClass: "group-hover:text-red-500",
    hoverScale: "group-hover:scale-125",
  },

  {
    name: "Winter",
    slug: "winter",
    icon: "/icons/winter.png",
    label: "WINTER",
    imageClass: "opacity-65",
    textClass: "group-hover:text-sky-300",
    hoverScale: "group-hover:scale-125",
  },
];

type FeaturedPerfume = {
  id: string;
  name: string;
  brand: string;
  main_image: string;
};

function capitalizeWords(text: string) {
  return text
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export default async function Home() {

  const response = await fetch("http://localhost:5500/parfurm/featured", {
    cache: "no-store",
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.log("FEATURED FETCH STATUS:", response.status);
    console.log("FEATURED FETCH BODY:", errorText);
    throw new Error(`Erro ao buscar os perfumes em destaque. Status: ${response.status}`);
  }

  const featuredPerfumes: FeaturedPerfume[] = await response.json();

  const visibleFeatured = featuredPerfumes.slice(0, 5);
  
  const infiniteFeatured = [...visibleFeatured, ...visibleFeatured];


return (

<main className="min-h-screen bg-gradient-to-b from-neutral-50 to-neutral-400">
    <div className="mx-auto max-w-6xl px-6 py-10">
    
        <header className="mb-14 text-center">
            <h1 className={`${quicksand.className} text-6xl font-light tracking-widest text-neutral-600`}>L’ÉLU PARFUMS</h1>       
            <h2 className={`${quicksand.className} mt-8 text-2xl font-light tracking-wide text-neutral-600`}>L’art de l'épanouissement</h2>
        </header>
    

        <section className="mx-auto max-w-6xl">
          <div className="grid grid-cols-2 gap-x-24 gap-y-20 md:grid-cols-4 md:gap-x-28 md:gap-y-24">
            
            {seasons.map((season) => (
              
              <Link
                key={season.slug}
                href={`/parfurm/seasons/${season.slug}`}
                className="group flex flex-col items-center">
        
                <div className="flex h-44 w-44 items-center justify-center rounded-2xl transition duration-300">         
                  <Image
                    src={season.icon}
                    alt={season.label}
                    width={130}
                    height={130}
                    className={`grayscale ${season.imageClass} transition duration-300 group-hover:scale-125 group-hover:grayscale-0 group-hover:opacity-100`}/>
                </div>

                <p className={`${quicksand.className} mt-5 text-base font-semibold uppercase tracking-[0.2em] text-transparent opacity-0 transition duration-300 ${season.textClass} group-hover:opacity-100`}>
                  {season.label}</p>

              </Link>
            ))}
          </div>
        </section>


        <section className="mx-auto mt-16 max-w-7xl overflow-hidden">

          <div className="featured-track flex gap-10">
            {infiniteFeatured.map((featuredItem, index) => (
      
              <Link
                key={`${featuredItem.id}-${index}`}
                href={`/parfurm/featured/${featuredItem.id}`}
                className="w-[330px] flex-shrink-0 rounded-2xl bg-black/15 p-4 transition hover:bg-black/15">

                <div className="relative aspect-[3/4] rounded-xl bg-neutral-200/60">

                  <Image
                    src={featuredItem.main_image}
                    alt={featuredItem.name}
                    fill
                    className="object-contain p-3"
                    sizes="(max-width: 1024px) 100vw, 330px"
                  />

                </div>

                <div className="mt-4 w-4/4 rounded-xl bg-neutral-200/60 px-3 py-2">
                  <p className={`${quicksand.className} text-sm text-neutral-800`}>
                    {capitalizeWords(featuredItem.name)}  {capitalizeWords(featuredItem.brand)}
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