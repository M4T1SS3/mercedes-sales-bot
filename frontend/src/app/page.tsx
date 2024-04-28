"use client";

import { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import "./app.css";
import "./../styles/chat.css";
import Image from "next/image";
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

const carPhotoMap: { [key: string]: StaticImageData } = {
  "EQE Sedan": EQE,
  "EQS Sedan": EQS,
  EQA: EQA,
  EQB: EQB,
  "EQE SUV": EQE_SUV,
  "EQS SUV": EQS_SUV,
  "G-Class Electric": G_Class,
  EQT: EQT,
  EQV: EQV,
};

const carVideoMap: { [key: string]: string } = {
  "EQE Sedan": "https://www.youtube.com/embed/8y0Sqg7gzS8?si=udb4oFdr6FT5xIYK",
  "EQS Sedan": "https://www.youtube.com/embed/vBAQ0fdn3sc?si=zht-E_1fjVs8fIug",
  EQA: "https://www.youtube.com/embed/N2nqwVSFkn0?si=ADYObHJAviVZwtuN",
  EQB: "https://www.youtube.com/embed/5VYKT6_KCCU?si=lj-PMJhFqltfBo0l",
  "EQE SUV": "https://www.youtube.com/embed/3WGGS_mwPTs?si=3jQMGokzsq-R5HYh",
  "EQS SUV": "https://www.youtube.com/embed/G1jGG7eziTA?si=QMHH0mLOO6lfEQ0Y",
  "G-Class Electric":
    "https://www.youtube.com/embed/mE_ZnkOgx8M?si=q8HiH-7TR4m6llGj",
  EQT: "https://www.youtube.com/embed/8DwH28d9DCM?si=P-0SgsBA3YHlRBbq",
  EQV: "https://www.youtube.com/embed/EP7OGJaf4aM?si=fHivKrRuJK64-kXA",
};

export default function Home() {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [message, setMessage] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null); // Session ID can be null initially
  const [carRecommendations, setCarRecommendations] = useState<string[]>([]); // Car recommendations are initially empty
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [showVideo, setShowVideo] = useState(false);
  const [videoIndex, setVideoIndex] = useState(0);

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
      const response = await fetch("https://carista-makeathon-f1e31d920312.herokuapp.com/chat", {
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
        setCarRecommendations(data.car_recommendations);
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

  // useEffect(() => {
  //   if (showVideo && carRecommendations.length > 0) {
  //     const firstRecommendation = carRecommendations[0];
  //     if (iframeRef.current) {
  //       const videoUrl = carVideoMap[firstRecommendation];
  //       const videoId = videoUrl.split("v=").pop();
  //       const iframeUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
  //       iframeRef.current.src = iframeUrl;
  //     }
  //   }
  // }, [showVideo, carRecommendations]);

  return (
    <main className="container mx-auto p-4 ">
      <h1 className="text-xl font-bold mb-2">Carista Chat Interface</h1>

      {chatHistory.length === 0 ? (
        <div className="no-messages">
          <div className="flex justify-center mb-4 chat-history">
            <h2 className="text-4xl font-mercedes">Talk to Carista: Your Mercedes-Benz EV Assistant</h2>
          </div>
        </div>
      ) : (
        <div ref={chatContainerRef} className="chat-history">
          {chatHistory.map((chat, index) => (
            <div key={index} className={`chat-message ${chat.role}`}>
              {chat.content}
              {chat.carRecommendations &&
                chat.carRecommendations.length > 0 && ( // Add this condition
                  <div>
                    <br />
                    <div className="car-recommendations">
                      {chat.carRecommendations.map((recommendation, index) => (
                        <div key={index} className="car-recommendation-panel">
                          <div className="car-recomendation-panel">
                            <h5>{recommendation.car_name}</h5>
                            <Image
                              src={carPhotoMap[recommendation.car_name]}
                              alt={recommendation.car_name}
                            />
                            <ul>
                              {recommendation.advantages.map(
                                (advantage, index) => (
                                  <li key={index}>{advantage}</li>
                                )
                              )}
                            </ul>
                            <button
                              className="video-button"
                              onClick={() => {
                                setShowVideo(true);
                                setVideoIndex(index);
                              }}
                            >
                              Watch Video
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
            </div>
          ))}
        </div>
      )}
      {/* Display chat history */}

      {/* {showVideo && (
        <div className="video-panel">
          <button className="close-button" onClick={() => setShowVideo(false)}>
            X
          </button>
          {carRecommendations.length > 0 ? (
            <iframe
              ref={iframeRef}
              width="100%"
              height="400"
              src={carVideoMap[carRecommendations[videoIndex].car_name]}
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
            />
          ) : (
            <p>No video available</p>
          )}
        </div>
      )} */}
      {showVideo && (
        <div
          className="video-panel"
          onClick={(e) => {
            if ((e.target as HTMLElement).className === "video-panel") {
              setShowVideo(false);
            }
          }}
        >
          <button className="close-button" onClick={() => setShowVideo(false)}>
            X
          </button>
          {carRecommendations.length > 0 ? (
            <iframe
              ref={iframeRef}
              width="100%"
              height="400"
              src={carVideoMap[carRecommendations[videoIndex].car_name]}
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
            />
          ) : (
            <p>No video available</p>
          )}
        </div>
      )}

      {/* Form for sending messages */}
      {/* <form onSubmit={handleSendMessage} className="mt-4 form-container">
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
      </form> */}
      {!showVideo && (
        <form onSubmit={handleSendMessage} className="mt-4 form-container">
          <input
            type="text"
            className="border p-2"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
          <button type="submit" className="text-white p-2 ml-2">
            Send
          </button>
        </form>
      )}
    </main>
  );
}
