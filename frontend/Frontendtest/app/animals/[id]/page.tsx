import { notFound } from 'next/navigation';

interface Animal {
    id: number;
    name: string;
    species: string;
    scientific_name: string;
    age: number | null;
    gender: "MALE" | "FEMALE" | "OTHER";
}

// Fetch a specific animal by ID
async function fetchAnimal(id: number): Promise<Animal | null> {
    const res = await fetch(`http://localhost:8000/api/profiles/${id}`, { cache: 'no-store' });
    if (!res.ok) {
        return null;
    }
    return res.json();
}

// Dynamic route props type
interface AnimalPageProps {
    params: Promise<{ id: string }>;
}

export default async function AnimalPage({ params }: AnimalPageProps) {
    const resolvedParams = await params; // Ensure params is resolved asynchronously
    const animalId = parseInt(resolvedParams.id, 10);

    if (isNaN(animalId)) {
        notFound();
    }

    const animal = await fetchAnimal(animalId);

    if (!animal) {
        notFound();
    }

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
            <h1>{animal.name}</h1>
            <p><strong>Species:</strong> {animal.species}</p>
            <p><strong>Scientific Name:</strong> {animal.scientific_name}</p>
            <p><strong>Age:</strong> {animal.age ?? 'Unknown'}</p>
            <p><strong>Gender:</strong> {animal.gender}</p>
        </div>
    );
}
