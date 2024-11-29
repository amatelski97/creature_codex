import React, { useMemo, useState, useEffect } from "react";
import axios from "axios";
import { MantineProvider, Container, Button, Title, FileInput } from "@mantine/core";
import { MantineReactTable, MRT_ColumnDef } from "mantine-react-table";

// Interface for Profile
interface Profile {
  id: number;
  name: string;
  species: string;
  scientific_name: string;
  age: number | null;
  gender: "MALE" | "FEMALE" | "OTHER";
}

const App: React.FC = () => {
  const [data, setData] = useState<Profile[]>([]);
  const [csvFile, setCsvFile] = useState<File | null>(null);

  const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";

  // Fetch data from the backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<Profile[]>(`${apiUrl}/profiles`);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [apiUrl]);

  // Handle CSV Upload
  const handleUpload = async () => {
    if (!csvFile) {
      alert("Please select a file to upload");
      return;
    }
    const formData = new FormData();
    formData.append("file", csvFile);

    try {
      const response = await axios.post(`${apiUrl}/profiles/upload_csv/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(response.data.message);
      // Refresh data after successful upload
      const updatedData = await axios.get<Profile[]>(`${apiUrl}/profiles`);
      setData(updatedData.data);
    } catch (error) {
      console.error("Error uploading CSV:", error);
      alert("Failed to upload CSV. Check the console for details.");
    }
  };

  // Define table columns
  const columns = useMemo<MRT_ColumnDef<Profile>[]>(
    () => [
      { accessorKey: "name", header: "Name" },
      { accessorKey: "species", header: "Species" },
      { accessorKey: "scientific_name", header: "Scientific Name" },
      { accessorKey: "age", header: "Age" },
      { accessorKey: "gender", header: "Gender" },
    ],
    []
  );

  return (
    <MantineProvider>
      <Container>
        <Title order={1} mb="lg">
          Animal Profiles
        </Title>
        <div>
          <div>
            <label>Choose a CSV file</label>
            <FileInput
              accept=".csv"
              onChange={(file) => setCsvFile(file)}
            />
          </div>
        </div>

        <Button mt="sm" onClick={handleUpload}>
          Upload
        </Button>
        <MantineReactTable columns={columns} data={data} />
      </Container>
    </MantineProvider>
  );
};

export default App;