import { useEffect, useState } from "react";
import API from "./api";

function App() {
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState({
    employee_id: "",
    full_name: "",
    email: "",
    department: ""
  });

  const fetchEmployees = async () => {
    const res = await API.get("/employees");
    setEmployees(res.data);
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await API.post("/employees", form);
    fetchEmployees();
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>HRMS Lite</h1>

      <h2>Add Employee</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Emp ID"
          onChange={(e)=>setForm({...form, employee_id:e.target.value})}/>
        <input placeholder="Full Name"
          onChange={(e)=>setForm({...form, full_name:e.target.value})}/>
        <input placeholder="Email"
          onChange={(e)=>setForm({...form, email:e.target.value})}/>
        <input placeholder="Department"
          onChange={(e)=>setForm({...form, department:e.target.value})}/>
        <button type="submit">Add</button>
      </form>

      <h2>Employees</h2>
      {employees.length === 0 ? <p>No employees</p> :
        employees.map(emp => (
          <div key={emp.id}>
            {emp.full_name} - {emp.department}
          </div>
        ))
      }
    </div>
  );
}

export default App;