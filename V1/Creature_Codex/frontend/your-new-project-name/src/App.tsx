
import React, { useMemo, useEffect, useState } from "react";
import axios from "axios";
import { Container, Title } from "@mantine/core";
import {
  MantineReactTable,
  type MRT_ColumnDef,
} from "mantine-react-table";
// Enum for Gender
export enum Gender {
  MALE = "MALE",
  FEMALE = "FEMALE",
  OTHER = "OTHER",
}
// Interface for Profile
interface Profile {
  id: number;
  name: string;
  age: number;
  species: string;
  scientific_name: string;
  gender: Gender;
}
const App: React.FC = () => {
  const [data, setData] = useState<Profile[]>([]);
  const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000/profiles/animal_profiles";
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<Profile[]>(apiUrl);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, [apiUrl]); // Include apiUrl in the dependency array
  // Memoize columns to prevent unnecessary re-renders
  const columns = useMemo<MRT_ColumnDef<Profile>[]>(
    () => [
      {
        accessorKey: "name",
        header: "Name",
      },
      {
        accessorKey: "species",
        header: "Species",
      },
      {
        accessorKey: "scientific_name",
        header: "Scientific Name",
      },
      {
        accessorKey: "age",
        header: "Age",
      },
      {
        accessorKey: "gender",
        header: "Gender",
        Cell: ({ cell }) => {
          const gender = cell.getValue<Gender>();
          return gender === Gender.MALE
            ? "Male"
            : gender === Gender.FEMALE
            ? "Female"
            : "Other";
        },
      },
    ],
    []
  );
  return (
    <Container>
      <Title order={1} mb="lg">
        Animal Profiles
      </Title>
      <MantineReactTable
        columns={columns}
        data={data}
        enablePagination
        enableSorting
        enableColumnFilters
      />
    </Container>
  );
};
export default App;
