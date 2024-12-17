"use client";
import { use, useState, useEffect } from "react";

type Animal = {
  id: number;
  name: string;
  species: string;
  scientific_name?: string;
  age?: number | null;
  gender: "MALE" | "FEMALE" | "OTHER";
  category: string;
  latest_record_date?: string;
  latest_weight?: number;
  latest_deep_clean?: string;
  latest_cleaner_name?: string;
};

export default function AnimalProfilePage({ params }: { params: Promise<{ category: string; id: string }> }) {
  const { category, id } = use(params); // Correctly unwrapping `params` using `use`

  const [animal, setAnimal] = useState<Animal | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id || !category) return;

    fetch(`http://localhost:8000/api/profiles/${category}/${id}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(
            `Failed to fetch profile with ID: ${id} and Category: ${category}`
          );
        }
        return res.json();
      })
      .then((data: Animal) => {
        setAnimal(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [id, category]);

  if (loading) {
    return <div>Loading animal profile...</div>;
  }

  if (error) {
    return <div>Error fetching animal profile: {error}</div>;
  }

  if (!animal) {
    return <div>No animal found for ID: {id} and Category: {category}.</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>{animal.name}</h1>
      <p><strong>ID:</strong> {animal.id}</p>
      <p><strong>Species:</strong> {animal.species}</p>
      <p><strong>Scientific Name:</strong> {animal.scientific_name ?? "N/A"}</p>
      <p><strong>Age:</strong> {animal.age ?? "Unknown"}</p>
      <p><strong>Gender:</strong> {animal.gender}</p>
      <p><strong>Category:</strong> {animal.category}</p>
      <p><strong>Current Weight:</strong> {animal.latest_weight}</p>
      <p><strong>Latest Weigh-in:</strong> {animal.latest_record_date ?? "N/A"}</p>
      <p><strong>Deep Clean Date:</strong> {animal.latest_deep_clean}</p>
      <p><strong>Cleaner Name:</strong> {animal.latest_cleaner_name}</p>
    </div>
  );
}
