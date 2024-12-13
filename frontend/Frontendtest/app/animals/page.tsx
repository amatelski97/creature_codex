"use client";

import { Card, Image, Text, Badge, Button, Group, Drawer } from '@mantine/core';
import { useState } from 'react';

type Animal = {
  id: number;
  name: string;
  species: string;
  scientific_name: string;
  age: number | null;
  gender: "MALE" | "FEMALE" | "OTHER";
};

async function fetchAnimals(): Promise<Animal[]> {
  const res = await fetch('http://localhost:8000/api/profiles/all', {
    cache: 'no-store',
  });

  if (!res.ok) {
    throw new Error('Failed to fetch animals');
  }

  return res.json();
}

export default function AnimalsPage() {
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAnimal, setSelectedAnimal] = useState<Animal | null>(null);
  const [drawerOpened, setDrawerOpened] = useState(false);

  useState(() => {
    fetchAnimals()
      .then((data) => {
        setAnimals(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, );

  if (loading) {
    return <div>Loading animals...</div>;
  }

  if (error) {
    return <div>Error fetching animals: {error}</div>;
  }

  if (!animals || animals.length === 0) {
    return <div>No animals found.</div>;
  }

  const handleViewDetails = (animal: Animal) => {
    setSelectedAnimal(animal);
    setDrawerOpened(true);
  };

  return (
    <>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px', padding: '20px' }}>
        {animals.map((animal) => (
          <Card key={animal.id} shadow="sm" padding="lg" radius="md" withBorder>
            <Card.Section>
              <Image
                src="/default-animal.jpg" // Replace with actual image if available
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

      {/* Drawer for Animal Details */}
      <Drawer
        opened={drawerOpened}
        onClose={() => setDrawerOpened(false)}
        title={selectedAnimal?.name}
        padding="md"
        size="lg"
        position="right"
      >
        {selectedAnimal ? (
          <div>
            <p><strong>Species:</strong> {selectedAnimal.species}</p>
            <p><strong>Scientific Name:</strong> {selectedAnimal.scientific_name}</p>
            <p><strong>Age:</strong> {selectedAnimal.age ?? 'Unknown'}</p>
            <p><strong>Gender:</strong> {selectedAnimal.gender}</p>
          </div>
        ) : (
          <p>No animal selected.</p>
        )}
      </Drawer>
    </>
  );
}
