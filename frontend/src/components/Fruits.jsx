import React, { useEffect, useState } from "react";
import api from "../api.js";
import AddFruitForm from "./AddFruitForm";
import DeleteIcon from "@mui/icons-material/Delete";
import ArrowRightSharpIcon from '@mui/icons-material/ArrowRightSharp';
const FruitList = () => {
  const [fruits, setFruits] = useState([]);

  const fetchFruits = async () => {
    try {
      const response = await api.get("/fruits");
      setFruits(response.data.fruits);
    } catch (error) {
      console.error("Error fetching fruits", error);
    }
  };

  const handleDelete = (id) => {
    api.delete(`/fruits/${id}`);
    window.location.reload();
  };

  const addFruit = async (fruitName) => {
    try {
      await api.post("/fruits", { name: fruitName });
      fetchFruits(); // Refresh the list after adding a fruit
    } catch (error) {
      console.error("Error adding fruit", error);
    }
  };

  useEffect(() => {
    fetchFruits();
  }, []);

  return (
    <div>
      <h2>Fruits List</h2>
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {fruits.map((fruit, index) => (
          <li
            key={index}
            style={{
              display: "flex",
              alignItems: "center",
              marginBottom: "10px",
            }}
          >
            <ArrowRightSharpIcon />
            <span style={{ flexGrow: 1 }}>{fruit.name}</span>{" "}
            {/* This will take the remaining space */}
            <button
              onClick={() => handleDelete(fruit.id)}
              style={{
                border: "none",
                background: "none",
                cursor: "pointer",
                padding: 0,
              }}
            >
              <DeleteIcon/>
            </button>
          </li>
        ))}
      </ul>
      <AddFruitForm addFruit={addFruit} />
    </div>
  );
};

export default FruitList;
