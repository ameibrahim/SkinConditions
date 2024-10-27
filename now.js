const user = [
  {
    id: "lz5smpqv",
    question: {
      english: "What is fire?",
      turkish: "Ateş nedir?",
    },
    answerOptions: {
      english: [
        "A form of light",
        "A type of gas",
        "A chemical reaction",
        "A type of solid",
      ],
      turkish: [
        "Işık formu",
        "Bir tür gaz",
        "Kimyasal bir tepkime",
        "Bir tür katı",
      ],
    },
    answer: {
      english: "A chemical reaction",
      turkish: "Bir kimyasal tepkime",
    },
    type: "multiple choice",
    hardness: "medium",
    marksWorth: 1,
  },
  {
    id: "lz5smpiq",
    question: {
      english: "What is fire?",
      turkish: "Ateş nedir?",
    },
    answerOptions: {
      english: [
        "A type of solid",
        "A form of water",
        "A type of energy",
        "A chemical compound",
      ],
      turkish: [
        "Bir tür katı",
        "Su formu",
        "Bir enerji türü",
        "Bir kimyasal bileşim",
      ],
    },
    answer: {
      english: "A type of energy",
      turkish: "Bir enerji türü",
    },
    type: "multiple choice",
    hardness: "medium",
    marksWorth: 1,
  },
  {
    id: "lz5smpy5",
    question: {
      english: "Fire is a chemical reaction between _____ and ______.",
      turkish: "Yanm bir kimyasal tepkime _____ ve ______ arasnda bir ksitr.",
    },
    answerOptions: {
      english: [
        "A. Oxygen, Fuel",
        "B. Water, Air",
        "C. Nitrogen, Carbon Dioxide",
        "D. Iron, Wood",
      ],
      turkish: [
        "A. Oksijen, Yaklt",
        "B. Su, Hava",
        "C. Azot, Karbondioksit",
        "D. Demir, Ay",
      ],
    },
    answer: {
      english: "A",
      turkish: "A",
    },
    type: "multiple choice",
    hardness: "hard",
    marksWorth: 1,
  },
  {
    id: "lz5smrsd",
    question: {
      english:
        "Which of the following is not a requirement for fire to occur: _____",
      turkish:
        "Aada listelenenlerden hangisi yanmann gzlenmesi iin bir gereklilik deildir: _____",
    },
    answerOptions: {
      english: ["A. Ignition Source", "B. Heat", "C. Oxygen", "D. Water"],
      turkish: ["A. Alglama kayna", "B. Scaklk", "C. Oksijen", "D. Su"],
    },
    answer: {
      english: "D",
      turkish: "D",
    },
    type: "multiple choice",
    hardness: "hard",
    marksWorth: 1,
  },
  {
    id: "lz5sml5l",
    question: {
      english: "Is fire a living organism?",
      turkish: "Ateş bir canlı organizma mıdır?",
    },
    answerOptions: {
      english: ["True", "False"],
      turkish: ["Doğru", "Yanlış"],
    },
    answer: {
      english: "False",
      turkish: "Yanlış",
    },
    type: "trueFalse",
    hardness: "hard",
    marksWorth: 1,
  },
  {
    id: "lz5smkyg",
    question: {
      english: "Can fire burn without oxygen present?",
      turkish: "Oksijen olmadan ateş yanabilir mi?",
    },
    answerOptions: {
      english: ["True", "False"],
      turkish: ["Doğru", "Yanlış"],
    },
    answer: {
      english: "False",
      turkish: "Yanlış",
    },
    type: "trueFalse",
    hardness: "hard",
    marksWorth: 1,
  },
];

user.forEach((s) => {
  console.log(s.question.english);
  console.log(s.question.turkish);
});
