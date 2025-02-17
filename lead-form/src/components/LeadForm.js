import React, { useState } from "react";
import "./LeadForm.css";

const LeadForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    loanAmount: "",
    loanTerm: "",
    interestRate: "5.99", // Default interest rate
    monthlyIncome: "",
  });

  const [result, setResult] = useState(null);
  const [step, setStep] = useState(1);
  const [submissionStatus, setSubmissionStatus] = useState("");

  const calculateLoan = () => {
    const principal = parseFloat(formData.loanAmount);
    const years = parseFloat(formData.loanTerm);
    const rate = parseFloat(formData.interestRate) / 100 / 12;
    const numberOfPayments = years * 12;

    const monthlyPayment = (
      (principal * rate * Math.pow(1 + rate, numberOfPayments)) /
      (Math.pow(1 + rate, numberOfPayments) - 1)
    ).toFixed(2);

    const totalPayment = (monthlyPayment * numberOfPayments).toFixed(2);
    const totalInterest = (totalPayment - principal).toFixed(2);

    return { monthlyPayment, totalPayment, totalInterest };
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const calculations = calculateLoan();
    setResult(calculations);
    setStep(2);
  };

  const handleLeadCaptureSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/api/leads/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          message: `Loan Amount: $${formData.loanAmount}, Loan Term: ${formData.loanTerm} years, Interest Rate: ${formData.interestRate}%`,
        }),
      });

      if (response.ok) {
        setSubmissionStatus("Lead submitted successfully!");
        // Optionally reset the form or handle success
      } else {
        setSubmissionStatus("Failed to submit lead.");
      }
    } catch (error) {
      console.error("Error submitting lead:", error);
      setSubmissionStatus("An error occurred while submitting the lead.");
    }
  };

  return (
    <div className="calculator-container">
      <div className="calculator-header">
        <h2>Loan Calculator</h2>
        <p className="subtitle">Get your personalized loan estimate today</p>
      </div>

      <div className="calculator-content">
        {step === 1 ? (
          <form onSubmit={handleSubmit} className="calculator-form">
            <div className="form-group">
              <label>Loan Amount ($)</label>
              <input
                type="number"
                name="loanAmount"
                value={formData.loanAmount}
                onChange={handleInputChange}
                required
                placeholder="Enter loan amount"
                className="form-input"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Loan Term (Years)</label>
                <input
                  type="number"
                  name="loanTerm"
                  value={formData.loanTerm}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter term"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Interest Rate (%)</label>
                <input
                  type="number"
                  name="interestRate"
                  value={formData.interestRate}
                  onChange={handleInputChange}
                  step="0.01"
                  required
                  className="form-input"
                />
              </div>
            </div>

            <button type="submit" className="calculate-button">
              Calculate Payment
            </button>
          </form>
        ) : (
          <div className="results-container">
            <div className="result-summary">
              <div className="result-item">
                <h3>Monthly Payment</h3>
                <p className="amount">${result.monthlyPayment}</p>
              </div>
              <div className="result-item">
                <h3>Total Payment</h3>
                <p className="amount">${result.totalPayment}</p>
              </div>
              <div className="result-item">
                <h3>Total Interest</h3>
                <p className="amount">${result.totalInterest}</p>
              </div>
            </div>

            <form onSubmit={handleLeadCaptureSubmit} className="lead-capture-form">
              <h3>Get Your Detailed Report</h3>
              <div className="form-group">
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Full Name"
                  required
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Email Address"
                  required
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="Phone Number"
                  required
                  className="form-input"
                />
              </div>
              <button type="submit" className="submit-button">
                Get Free Report
              </button>
              {submissionStatus && <p className="submission-status">{submissionStatus}</p>}
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default LeadForm;
