import React, { useState } from "react";

function App() {
	const [country, setCountry] = useState("");
	const [state, setState] = useState("");
	const [city, setCity] = useState("");
	const [result, setResult] = useState(null);

	const predictAQI = async () => {
		const res = await fetch("http://localhost:7860/predict", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ country, state, city }),
		});

		const data = await res.json();
		setResult(data);
	};

	return (
		<div style={{ padding: 20 }}>
			<h2>AQI Predictor</h2>
			<input
				placeholder="Country"
				onChange={(e) => setCountry(e.target.value)}
			/>
			<input placeholder="State" onChange={(e) => setState(e.target.value)} />
			<input placeholder="City" onChange={(e) => setCity(e.target.value)} />
			<button onClick={predictAQI}>Predict AQI</button>

			{result && (
				<div style={{ marginTop: 20 }}>
					<h3>Results:</h3>
					<p>🌡 Predicted AQI: {result.predicted_aqi.toFixed(2)}</p>
					<p>📊 Actual AQI (IQAir): {result.actual_aqi}</p>
					<h4>Features Used:</h4>
					<ul>
						{Object.entries(result.features).map(([key, value]) => (
							<li key={key}>
								{key}: {value}
							</li>
						))}
					</ul>
				</div>
			)}
		</div>
	);
}

export default App;
