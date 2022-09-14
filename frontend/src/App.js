// author Ozgur Tarim

import axios from "axios"
import {format} from "date-fns";
import {useEffect, useState} from 'react';
import './App.css';
import logo from './logo.png'; 

//allows to access an API
const apiURL = "http://localhost:5000"

//allows data tracking in app
function App() {
  const [description, setDescription] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [eventsList, setEventsList] = useState([]);
  const [eventId, setEventId] = useState(null);

  const fetchEvents = async () => {
    const data= await axios.get(`${apiURL}/events`)
    const {events} = data.data
    setEventsList(events);
   
    }
    
  
  //for adding users tweets 
  const handleChange = (e, field) => {
    setDescription(e.target.value);
  }
  
  //for comments but not worked
  const handleEdit = (event ) => {
    setEventId(event.id);
    setEditDescription(event.description);
  }
    
  //for submit works
    const handleSubmit = async e => {
      e.preventDefault();
      try{
      let config = {
        headers: {
          "Access-Control-Allow-Origin": "*"
        }
      }
      //transforms the data returned from the server
      const data = await axios.post(`${apiURL}/events`, {description}, config)
      setEventsList([...eventsList, data.data]);
      setDescription('');

      }catch (err) {
        console.error(err.message);
      }

    }


    useEffect(() => {
      fetchEvents();

    }, [])

    



  return (
    <div className="App">
      <section>
      <div class="logo">
          <img src={logo} alt="Logo"/>
            </div>
         <form onSubmit={handleSubmit}>
          <label htmlFor = "description">Welcome to Chess Players Social App</label>
          <input
           onChange= {handleChange}
           type="text"
           name="description"
           id="description"
           placeholder = "Write about chess here"
           value={description}
          />
          <button type= "submit">Share</button>
        </form>
        </section>
        <section>
           <ul>
            {eventsList.map(event => {
              return(
                <li style={{display: "flex"}} key={event.id}>
                  {format(new Date(event.created_at), "MM/dd, p")}: {" "}
                  {event.description}
                  <button on Click = {() => handleEdit(event.id)} > Comment </button>
                </li>
              )
            })}

            </ul>
          </section>
          
      </div>
  );
}

export default App;
