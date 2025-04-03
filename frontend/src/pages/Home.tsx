import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [userType, setUserType] = useState("");
  const navigate = useNavigate();

  const handleNext = () => {
    if (userType === "student") {
      navigate("/upload-student");
    } else if (userType === "general") {
      navigate("/upload-general");
    }
  };

  return (
    <div style={{ padding: "4rem", textAlign: "center" }}>
      <h1>AI 지원금 문서 분석기</h1>
      <p>당신은 누구인가요?</p>
      <div style={{ margin: "2rem" }}>
        <label>
          <input
            type="radio"
            value="student"
            checked={userType === "student"}
            onChange={(e) => setUserType(e.target.value)}
          />
          학생
        </label>
        &nbsp;&nbsp;
        <label>
          <input
            type="radio"
            value="general"
            checked={userType === "general"}
            onChange={(e) => setUserType(e.target.value)}
          />
          일반인
        </label>
      </div>
      <button disabled={!userType} onClick={handleNext}>
        다음으로 →
      </button>
    </div>
  );
};

export default Home;
