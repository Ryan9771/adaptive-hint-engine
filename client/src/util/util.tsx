import axios from "axios";
import { TestResult } from "./types";

async function post(url = "", data = {}, token = "") {
  const response = await fetch(
    `https://adaptive-hint-generator-629e95ca5085.herokuapp.com${url}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(data),
    }
  );

  return response;
}

async function getExerciseDetails(studentName: string, exerciseId: string) {
  const response = await post(`/exercise/${studentName}/${exerciseId}`);

  const exerciseDetails = {
    exerciseExists: false,
    exerciseTitle: "",
    exerciseDescription: "",
    exerciseText: "",
    skelCode: "",
    previousCode: "",
  };

  console.log("Response: ", response);

  if (response.ok) {
    const data = await response.json();
    /*
    Received Response format:
    {
      "exercise_title": string
      "exercise_text": string
      "skel_code": string
      "exercise_background": string
    }
    */
    exerciseDetails.exerciseExists = true;
    exerciseDetails.exerciseTitle = data.exercise_title;
    exerciseDetails.exerciseDescription = data.exercise_background;
    exerciseDetails.exerciseText = data.exercise_text;
    exerciseDetails.skelCode = data.skel_code;
    exerciseDetails.previousCode = data.previous_code;
  } else {
    console.log("Failed to fetch entry");
  }

  return exerciseDetails;
}

async function resetPreviousCode(
  studentName: string,
  exerciseId: string,
  skelCode: string
) {
  const response = await post(`/exercise/reset/${studentName}/${exerciseId}`, {
    skel_code: skelCode,
  });

  if (response.ok) {
    console.log("Previous code reset successfully");
  } else {
    console.log("Failed to reset previous code");
  }
}

async function getHint(
  studentName: string,
  exerciseId: string,
  studentCode: string,
  error: string,
  testResults: TestResult[]
) {
  const response = await post(`/exercise/hint/${studentName}/${exerciseId}`, {
    studentCode: studentCode,
    error: error,
    testResults: testResults,
  });

  if (response.ok) {
    const data = await response.json();

    return {
      hint: data.hint,
      simpleHint: data.simpleHint,
    };
  }

  console.log("Failed to retreive hint");

  return {
    hint: "Seems like I was unable to generate a hint. Please try again.",
    simpleHint: "",
  };
}

const executePythonCode = async (code: string) => {
  try {
    const response = await axios.post(
      "https://emkc.org/api/v2/piston/execute",
      {
        language: "python",
        version: "3.10.0",
        files: [
          {
            name: "main.py",
            content: code,
          },
        ],
      }
    );

    const { run } = response.data;

    let output = "";
    let error = "";

    if (run.stdout) {
      output = run.stdout;
    }
    if (run.stderr) {
      error = run.stderr;
    }

    return {
      output: output,
      error: error,
    };
  } catch (error) {
    console.error("Error executing code:", error);

    return {
      output: "I was not able to execute this code, please try again.",
      error: "",
    };
  }
};

const testStudentCode = async (
  studentName: string,
  exerciseId: string,
  studentCode: string
) => {
  try {
    const response = await post(`/exercise/test/${studentName}/${exerciseId}`, {
      studentCode: studentCode,
    });

    if (response.ok) {
      const data = await response.json();

      return data;
    }
  } catch (error) {
    console.error("Error executing tests:", error);
    return {
      testResults: [],
    };
  }
};

const logEvaluation = async (
  studentName: string,
  exerciseId: string,
  hintRating: number,
  simpleHintRating: number,
  hintText: string,
  simpleHintText: string
) => {
  try {
    const response = await post(
      `/exercise/evaluation/${studentName}/${exerciseId}`,
      {
        hintRating: hintRating,
        simpleHintRating: simpleHintRating,
        hintText: hintText,
        simpleHintText: simpleHintText,
      }
    );

    if (response.ok) {
      console.log("Evaluation logged successfully");
    } else {
      console.log("Failed to log evaluation");
    }
  } catch (error) {
    console.error("Error logging evaluation:", error);
  }
};

export {
  post,
  getExerciseDetails,
  resetPreviousCode,
  getHint,
  executePythonCode,
  testStudentCode,
  logEvaluation,
};
