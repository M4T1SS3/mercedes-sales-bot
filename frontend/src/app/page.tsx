"use client";

import { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import "./app.css";
import "./../styles/chat.css";
import  Image  from "next/image"
import EQE from "../car_pics/EQE.png";
import EQS from "../car_pics/EQS.png";
import EQA from "../car_pics/EQA.png";
import EQB from "../car_pics/EQB.png";
import EQE_SUV from "../car_pics/EQE_SUV.png";
import EQS_SUV from "../car_pics/EQS_SUV.png";
import G_Class from "../car_pics/G-Class.png";
import EQT from "../car_pics/EQT.png";
import EQV from "../car_pics/EQV.png";
import { StaticImageData } from "next/image";

type CarRecommendation = {
  car_name: string;
  advantages: string[];
};

type ChatMessage = {
  role: string;
  content: string;
  carRecommendations?: CarRecommendation[];
};

// const carPhotoMap = {
//   "EQE Sedan": require("../car_pics/EQE.png"),
//   "EQS Sedan": require("../car_pics/EQS.png"),
//   "EQA": require("../car_pics/EQA.png"),
//   "EQB": require("../car_pics/EQB.png"),
//   "EQE SUV": require("../car_pics/EQE_SUV.png"),
//   "EQS SUV": require("../car_pics/EQS_SUV.png"),
//   "G-Class Electric": require("../car_pics/G-Class.png"),
//   "EQT": require("../car_pics/EQT.png"),
//   "EQV": require("../car_pics/EQV.png"),
// };

const carPhotoMap: { [key: string]: StaticImageData } = {
  "EQE Sedan": EQE,
  "EQS Sedan": EQS,
  "EQA": EQA,
  "EQB": EQB,
  "EQE SUV": EQE_SUV,
  "EQS SUV": EQS_SUV,
  "G-Class Electric": G_Class,
  "EQT": EQT,
  "EQV": EQV,
};

export default function Home() {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [message, setMessage] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null); // Session ID can be null initially
  const [carRecommendations, setCarRecommendations] = useState<string[]>([]); // Car recommendations are initially empty
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Set a random UUID when the component is first rendered
  useEffect(() => {
    if (!sessionId) {
      setSessionId(uuidv4()); // Generate a new UUID if it's null
    }
  }, [sessionId]); // Run only when sessionId is null

  const handleSendMessage = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!sessionId) {
      console.error("Session ID is missing");
      return;
    }
    setChatHistory((prev) => [...prev, { role: "user", content: message }]);
    setMessage(""); // Clear the message field
    //Remove car recommendations
    setCarRecommendations([]);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: message,
          car_recommendations: carRecommendations,
        }),
      });

      if (response.ok) {
        // Ensure the request was successful
        const data = await response.json(); // Parse the response

        // Update chat history
        setChatHistory((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.response,
            carRecommendations: data.car_recommendations,
          },
        ]);

        setMessage(""); // Clear the message field
      } else {
        console.error("Failed to fetch response from backend");
      }
    } catch (error) {
      console.error("Error occurred:", error);
    }
  };
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-xl font-bold mb-2">Basic Chat Interface</h1>

      {/* Display chat history */}
      <div ref={chatContainerRef} className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className={`chat-message ${chat.role}`}>
            {chat.content}
            {chat.carRecommendations &&
              chat.carRecommendations.length > 0 && ( // Add this condition
                <div>
                  <br />
                  {/* <h4>Car Recommendations</h4> */}
                  {/* <ul>
                    {chat.carRecommendations.map((recommendation, index) => (
                      <li key={index}>
                        <h5>{recommendation.car_name}</h5>
                        <ul>
                          {recommendation.advantages.map((advantage, index) => (
                            <li key={index}>{advantage}</li>
                          ))}
                        </ul>
                      </li>
                    ))}
                  </ul> */}
                  {/* <table>
                    <thead>
                      <tr>
                        <th>Car Name</th>
                        <th>Advantages</th>
                      </tr>
                    </thead>
                    <tbody>
                      {chat.carRecommendations.map((recommendation, index) => (
                        <tr key={index}>
                          <td>{recommendation.car_name}</td>
                          <td>
                            <ul
                              style={{
                                listStyle: "disc",
                                padding: 10,
                                paddingLeft: 25,
                                margin: 0,
                              }}
                            >
                              {recommendation.advantages.map(
                                (advantage, index) => (
                                  <li
                                    key={index}
                                    style={{ display: "list-item" }}
                                  >
                                    {advantage}
                                  </li>
                                )
                              )}
                            </ul>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table> */}
                  <div className="car-recommendations">
                    {chat.carRecommendations.map((recommendation, index) => (
                      <div key={index} className="car-recommendation-panel">
                        <h5>{recommendation.car_name}</h5>
                        <Image src={carPhotoMap[recommendation.car_name]} alt={recommendation.car_name} />
                        <ul>
                          {recommendation.advantages.map((advantage, index) => (
                            <li key={index}>{advantage}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        ))}
      </div>

      {/* Form for sending messages */}
      <form onSubmit={handleSendMessage} className="mt-4 form-container">
        <input
          type="text"
          className="border p-2"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
        />
        <button type="submit" className="bg-blue-500 text-white p-2 ml-2">
          Send
        </button>
      </form>
    </main>
  );
}
