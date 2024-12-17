"use client";

import { Card, Image, Text, Badge, Button, Group, Drawer } from "@mantine/core";
import { useState, useEffect } from "react";
import ModalForm from "../../components/WeightForm/ModalForm"; // Adjust the path based on your file structure

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

async function fetchAnimals(): Promise<Animal[]> {
  const res = await fetch("http://localhost:8000/api/profiles/all", {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch animals");
  }

  const data = await res.json();
  console.log("Fetched Animals:", data); // Debug log
  return data;
}

export default function AnimalsPage() {
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAnimal, setSelectedAnimal] = useState<Animal | null>(null);
  const [drawerOpened, setDrawerOpened] = useState(false);

  useEffect(() => {
    fetchAnimals()
      .then((data) => {
        setAnimals(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []); // UseEffect for data fetching

  const handleViewDetails = (animal: Animal) => {
    console.log("Selected Animal:", animal); // Debug log
    setSelectedAnimal(animal);
    setDrawerOpened(true);
  };

  if (loading) {
    return <div>Loading animals...</div>;
  }

  if (error) {
    return <div>Error fetching animals: {error}</div>;
  }

  if (!animals || animals.length === 0) {
    return <div>No animals found.</div>;
  }

  return (
    <>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "10px",
          padding: "20px",
        }}
      >
        {animals.map((animal) => (
          <Card key={animal.id} shadow="sm" padding="lg" radius="md" withBorder>
            <Card.Section>
              <Image
                src="/default-animal.jpg"
                alt={animal.name}
                height={160}
              />
            </Card.Section>

            <Group align="apart" mt="md" mb="xs">
              <Text fw={500}>{animal.name}</Text>
              <Badge color="green" variant="light">
                {animal.gender}
              </Badge>
            </Group>

            <Text size="sm" color="dimmed">
              <strong>Species:</strong> {animal.species}
            </Text>
            <Text size="sm" color="dimmed">
              <strong>Scientific Name:</strong> {animal.scientific_name}
            </Text>

            <Button
              variant="light"
              color="blue"
              fullWidth
              mt="md"
              radius="md"
              onClick={() => handleViewDetails(animal)}
            >
              View Details
            </Button>
          </Card>
        ))}
      </div>

      <Drawer
        opened={drawerOpened}
        onClose={() => setDrawerOpened(false)}
        title={selectedAnimal?.name}
        padding="md"
        size="lg"
        position="right"
      >
        {selectedAnimal ? (
          <div style={{ padding: "20px" }}>
            <h1>{selectedAnimal.name}</h1>
            <p>
              <strong>ID:</strong> {selectedAnimal.id}
            </p>
            <p>
              <strong>Species:</strong> {selectedAnimal.species}
            </p>
            <p>
              <strong>Scientific Name:</strong>{" "}
              {selectedAnimal.scientific_name ?? "N/A"}
            </p>
            <p>
              <strong>Age:</strong> {selectedAnimal.age ?? "Unknown"}
            </p>
            <p>
              <strong>Gender:</strong> {selectedAnimal.gender}
            </p>
            <p>
              <strong>Category:</strong> {selectedAnimal.category}
            </p>
            <hr style={{ margin: "20px 0" }} />
            <Group justify="space-between" align="center">
  <p><strong>Current Weight:</strong> {selectedAnimal.latest_weight ?? "N/A"}</p>
  <ModalForm
    title={`Update Weight for ${selectedAnimal.name}`}
    animalId={selectedAnimal.id}
    onSubmit={async (values) => {
      try {
        console.log("Weight Form Submitted:", values);

        // Send the data to the backend
        const res = await fetch("http://localhost:8000/api/weights", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        });

        if (!res.ok) {
          throw new Error("Failed to submit weight.");
        }

        alert("Weight updated successfully!");
      } catch (err) {
        console.error(err);
        alert("Error updating weight.");
      }
    }}
  />
</Group>

            <p>
              <strong>Latest Weigh In:</strong>{" "}
              {selectedAnimal.latest_record_date ?? "N/A"}
            </p>
            <hr style={{ margin: "20px 0" }} />
            <p>
              <strong>Deep Clean Date:</strong>{" "}
              {selectedAnimal.latest_deep_clean ?? "N/A"}
            </p>
            <p>
              <strong>Who Cleaned:</strong>{" "}
              {selectedAnimal.latest_cleaner_name ?? "N/A"}
            </p>
          </div>
        ) : (
          <p>No animal selected.</p>
        )}
      </Drawer>
    </>
  );
}
