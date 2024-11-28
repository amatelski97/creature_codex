import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const App = () => {
  const [data, setData] = useState([]);
  const [formData, setFormData] = useState({ name: "", age: "", species: "", scientific_name: "", gender: "" });
  const [searchData, setSearchData] = useState({ name: "", species: "", scientific_name: "", gender: "" });
  const [editId, setEditId] = useState(null);

  const apiUrl = "http://localhost:8000/profiles/animal_profiles"; // Replace with your FastAPI URL

  // Fetch data from FastAPI
  const fetchData = async () => {
    try {
      const response = await axios.get(apiUrl);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // Add new profile
  const addProfile = async () => {
    try {
      const response = await axios.post(apiUrl, formData);
      setData([...data, response.data]); // Add new profile to the table
      setFormData({ name: "", age: "", species: "", scientific_name: "", gender: "" }); // Reset form
    } catch (error) {
      console.error("Error adding profile:", error);
    }
  };

  // Update profile
  const updateProfile = async () => {
    try {
      const response = await axios.put(`${apiUrl}/${editId}`, formData);
      setData(
        data.map((profile) =>
          profile.id === editId ? { ...profile, ...response.data } : profile
        )
      );
      setEditId(null); // Exit edit mode
      setFormData({ name: "", age: "", species: "", scientific_name: "", gender: "" }); // Reset form
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  // Delete profile
  const deleteProfile = async (id) => {
    try {
      await axios.delete(`${apiUrl}/${id}`);
      setData(data.filter((profile) => profile.id !== id)); // Remove profile from the table
    } catch (error) {
      console.error("Error deleting profile:", error);
    }
  };

  // Search profiles
  const searchProfiles = async () => {
    try {
      const response = await axios.get(`${apiUrl}/search`, { params: searchData });
      setData(response.data);
    } catch (error) {
      console.error("Error searching profiles:", error);
    }
  };

  // Handle form change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle search form change
  const handleSearchInputChange = (e) => {
    const { name, value } = e.target;
    setSearchData({ ...searchData, [name]: value });
  };

  // Submit form for Add or Update
  const handleSubmit = (e) => {
    e.preventDefault();
    if (editId) {
      updateProfile();
    } else {
      addProfile();
    }
  };

  // Submit search form
  const handleSearchSubmit = (e) => {
    e.preventDefault();
    searchProfiles();
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="container">
      <h1>Animal Profiles</h1>
      <form onSubmit={handleSearchSubmit}>
        <div className="form-group">
          <label>Search Name</label>
          <input
            type="text"
            className="form-control"
            name="name"
            value={searchData.name}
            onChange={handleSearchInputChange}
          />
        </div>
        <div className="form-group">
          <label>Search Species</label>
          <input
            type="text"
            className="form-control"
            name="species"
            value={searchData.species}
            onChange={handleSearchInputChange}
          />
        </div>
        <div className="form-group">
          <label>Search Scientific Name</label>
          <input
            type="text"
            className="form-control"
            name="scientific_name"
            value={searchData.scientific_name}
            onChange={handleSearchInputChange}
          />
        </div>
        <div className="form-group">
          <label>Search Gender</label>
          <select
            className="form-control"
            name="gender"
            value={searchData.gender}
            onChange={handleSearchInputChange}
          >
            <option value="">Select Gender</option>
            <option value="MALE">Male</option>
            <option value="FEMALE">Female</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary">Search</button>
      </form>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name</label>
          <input
            type="text"
            className="form-control"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Age</label>
          <input
            type="number"
            className="form-control"
            name="age"
            value={formData.age}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Species</label>
          <input
            type="text"
            className="form-control"
            name="species"
            value={formData.species}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Scientific Name</label>
          <input
            type="text"
            className="form-control"
            name="scientific_name"
            value={formData.scientific_name}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Gender</label>
          <select
            className="form-control"
            name="gender"
            value={formData.gender}
            onChange={handleInputChange}
          >
            <option value="">Select Gender</option>
            <option value="MALE">Male</option>
            <option value="FEMALE">Female</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary">
          {editId ? "Update Profile" : "Add Profile"}
        </button>
      </form>
      <table className="table mt-4">
        <thead>
          <tr>
            <th>Name</th>
            <th>Species</th>
            <th>Scientific Name</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((profile) => (
            <tr key={profile.id}>
              <td>{profile.name}</td>
              <td>{profile.species}</td>
              <td>{profile.scientific_name}</td>
              <td>{profile.age}</td>
              <td>{profile.gender}</td>
              <td>
                <button
                  className="btn btn-warning mr-2"
                  onClick={() => {
                    setEditId(profile.id);
                    setFormData({
                      name: profile.name,
                      age: profile.age,
                      species: profile.species,
                      scientific_name: profile.scientific_name,
                      gender: profile.gender,
                    });
                  }}
                >
                  Edit
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => deleteProfile(profile.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;