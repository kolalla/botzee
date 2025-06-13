import React, { useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  TextInput,
} from 'react-native';
import { useRef } from 'react';

// Types for scorecard
type ScoreCategory = 'ones' | 'twos' | 'threes' | 'fours' | 'fives' | 'sixes' |
                   'threeOfAKind' | 'fourOfAKind' | 'fullHouse' | 'smallStraight' |
                   'largeStraight' | 'yahtzee' | 'chance';

type PlayerScores = {
  [key in ScoreCategory]: number | null;
};

type ChatMessage = {
  id: string;
  sender: 'player' | 'botzee';
  text: string;
  timestamp: Date;
};

// Game state management
const App = () => {
  const [currentPlayer, setCurrentPlayer] = useState('Player 1');
  const [rollsLeft, setRollsLeft] = useState(3);
  const [currentDice, setCurrentDice] = useState<number[]>([]);
  const [selectedDice, setSelectedDice] = useState<number[]>([]);
  const [gameStarted, setGameStarted] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'botzee',
      text: 'Ready to play! Tap \'Roll Dice\' to start.',
      timestamp: new Date()
    }
  ]);
  const chatScrollRef = useRef<ScrollView>(null);

  // Scorecard state
  const [scores, setScores] = useState<{[player: string]: PlayerScores}>({
    'Player 1': {
      ones: null, twos: null, threes: null, fours: null, fives: null, sixes: null,
      threeOfAKind: null, fourOfAKind: null, fullHouse: null, smallStraight: null,
      largeStraight: null, yahtzee: null, chance: null
    },
    'Player 2': {
      ones: null, twos: null, threes: null, fours: null, fives: null, sixes: null,
      threeOfAKind: null, fourOfAKind: null, fullHouse: null, smallStraight: null,
      largeStraight: null, yahtzee: null, chance: null
    },
    'Botzee': {
      ones: null, twos: null, threes: null, fours: null, fives: null, sixes: null,
      threeOfAKind: null, fourOfAKind: null, fullHouse: null, smallStraight: null,
      largeStraight: null, yahtzee: null, chance: null
    }
  });

  const rollDice = () => {
    const newDice = Array.from({ length: 5 }, () => Math.floor(Math.random() * 6) + 1);
    setCurrentDice(newDice);
    setRollsLeft(rollsLeft - 1);
    setGameStarted(true);
    setSelectedDice([]);
  };

  const toggleDiceSelection = (index: number) => {
    if (selectedDice.includes(index)) {
      setSelectedDice(selectedDice.filter(i => i !== index));
    } else {
      setSelectedDice([...selectedDice, index]);
    }
  };

  const rerollDice = () => {
    if (rollsLeft > 0) {
      const newDice = [...currentDice];
      for (let i = 0; i < 5; i++) {
        if (!selectedDice.includes(i)) {
          newDice[i] = Math.floor(Math.random() * 6) + 1;
        }
      }
      setCurrentDice(newDice);
      setRollsLeft(rollsLeft - 1);
    }
  };

  // Score calculation functions
  const calculateScore = (category: ScoreCategory, dice: number[]): number => {
    if (dice.length === 0) return 0;
    
    const counts: {[key: number]: number} = {};
    dice.forEach(die => {
      counts[die] = (counts[die] || 0) + 1;
    });
    
    const uniqueValues = Object.keys(counts).map(Number).sort((a, b) => a - b);
    const countValues = Object.values(counts).sort((a, b) => b - a);
    
    switch (category) {
      case 'ones': return dice.filter(d => d === 1).reduce((a, b) => a + b, 0);
      case 'twos': return dice.filter(d => d === 2).reduce((a, b) => a + b, 0);
      case 'threes': return dice.filter(d => d === 3).reduce((a, b) => a + b, 0);
      case 'fours': return dice.filter(d => d === 4).reduce((a, b) => a + b, 0);
      case 'fives': return dice.filter(d => d === 5).reduce((a, b) => a + b, 0);
      case 'sixes': return dice.filter(d => d === 6).reduce((a, b) => a + b, 0);
      case 'threeOfAKind': 
        return countValues[0] >= 3 ? dice.reduce((a, b) => a + b, 0) : 0;
      case 'fourOfAKind': 
        return countValues[0] >= 4 ? dice.reduce((a, b) => a + b, 0) : 0;
      case 'fullHouse': 
        return (countValues.length === 2 && countValues[0] === 3 && countValues[1] === 2) ? 25 : 0;
      case 'smallStraight': {
        const straights = [[1,2,3,4], [2,3,4,5], [3,4,5,6]];
        return straights.some(straight => straight.every(num => uniqueValues.includes(num))) ? 30 : 0;
      }
      case 'largeStraight': {
        const straights = [[1,2,3,4,5], [2,3,4,5,6]];
        return straights.some(straight => straight.every(num => uniqueValues.includes(num)) && straight.length === uniqueValues.length) ? 40 : 0;
      }
      case 'yahtzee': 
        return countValues[0] === 5 ? 50 : 0;
      case 'chance': 
        return dice.reduce((a, b) => a + b, 0);
      default: 
        return 0;
    }
  };

  const scoreCategory = (category: ScoreCategory) => {
    if (currentDice.length === 0 || scores[currentPlayer][category] !== null) return;
    
    const score = calculateScore(category, currentDice);
    setScores(prev => ({
      ...prev,
      [currentPlayer]: {
        ...prev[currentPlayer],
        [category]: score
      }
    }));
    
    // End turn
    setRollsLeft(3);
    setCurrentDice([]);
    setSelectedDice([]);
    setGameStarted(false);
    
    // Switch to next player (simplified)
    const players = ['Player 1', 'Player 2', 'Botzee'];
    const currentIndex = players.indexOf(currentPlayer);
    setCurrentPlayer(players[(currentIndex + 1) % players.length]);
  };

  const getPotentialScore = (category: ScoreCategory): number => {
    if (currentDice.length === 0) return 0;
    return calculateScore(category, currentDice);
  };

  const isScoreAvailable = (category: ScoreCategory): boolean => {
    return scores[currentPlayer][category] === null;
  };

  const sendMessage = () => {
    if (chatInput.trim() === '') return;
    
    // Add player message
    const playerMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'player',
      text: chatInput.trim(),
      timestamp: new Date()
    };
    
    setChatMessages(prev => [...prev, playerMessage]);
    setChatInput('');
    
    // Scroll to bottom after player message
    setTimeout(() => {
      chatScrollRef.current?.scrollToEnd({ animated: true });
    }, 100);
    
    // Add Botzee response after a short delay
    setTimeout(() => {
      const botzeeMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'botzee',
        text: "I'm still learning!",
        timestamp: new Date()
      };
      setChatMessages(prev => [...prev, botzeeMessage]);
      
      // Scroll to bottom after Botzee response
      setTimeout(() => {
        chatScrollRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }, 500);
  };

  // Show all messages but auto-scroll to bottom

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#ffffff" />
      <ScrollView style={styles.scrollView}>
        
        {/* Turn Info */}
        <View style={styles.turnInfo}>
          <Text style={styles.turnInfoText}>{currentPlayer}</Text>
          <TouchableOpacity 
            style={[styles.rollButton, !gameStarted || rollsLeft === 0 ? styles.rollButtonDisabled : null]}
            onPress={gameStarted ? rerollDice : rollDice}
            disabled={rollsLeft === 0}
          >
            <Text style={styles.turnInfoText}>
              {!gameStarted ? '🎲 Roll Dice' : rollsLeft > 0 ? '🎲 Next Roll' : '🎯 Choose a score!'}
            </Text>
          </TouchableOpacity>
          <Text style={styles.turnInfoText}>Rolls left: {rollsLeft}</Text>
        </View>

        {/* Dice Section */}
        <View style={styles.diceContainer}>
          <View style={styles.diceGrid}>
            {Array.from({ length: 5 }, (_, index) => (
              <TouchableOpacity
                key={index}
                style={[
                  styles.die,
                  currentDice[index] ? null : styles.dieEmpty,
                  selectedDice.includes(index) ? styles.dieSelected : null
                ]}
                onPress={() => currentDice[index] && toggleDiceSelection(index)}
                disabled={!currentDice[index]}
              >
                <Text style={[
                  styles.dieText,
                  !currentDice[index] ? styles.dieTextEmpty : null
                ]}>
                  {currentDice[index] || '?'}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Scorecard */}
        <View style={styles.scorecard}>
          <View style={styles.scorecardHeader}>
            <View style={styles.scorecardRow}>
              <Text style={styles.scorecardHeaderText}></Text>
              <Text style={[styles.scorecardHeaderText, styles.scorecardHeaderCenter]}>{currentPlayer === 'Player 1' ? '🎯 ' : ''}Player 1</Text>
              <Text style={[styles.scorecardHeaderText, styles.scorecardHeaderCenter]}>{currentPlayer === 'Player 2' ? '🎯 ' : ''}Player 2</Text>
              <Text style={[styles.scorecardHeaderText, styles.scorecardHeaderCenter]}>{currentPlayer === 'Botzee' ? '🎯 ' : ''}Botzee</Text>
            </View>
          </View>

          {/* Upper Section */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>UPPER SECTION</Text>
          </View>
          
          {[{name: 'Ones', key: 'ones'}, {name: 'Twos', key: 'twos'}, {name: 'Threes', key: 'threes'}, 
            {name: 'Fours', key: 'fours'}, {name: 'Fives', key: 'fives'}, {name: 'Sixes', key: 'sixes'}].map((category) => (
            <View key={category.key} style={styles.scorecardRow}>
              <Text style={styles.categoryName}>{category.name}</Text>
              {['Player 1', 'Player 2', 'Botzee'].map(player => {
                const score = scores[player][category.key as ScoreCategory];
                const isCurrentPlayer = player === currentPlayer;
                const potential = isCurrentPlayer && currentDice.length > 0 && score === null ? getPotentialScore(category.key as ScoreCategory) : null;
                
                return (
                  <TouchableOpacity 
                    key={player}
                    style={[styles.scoreCell, isCurrentPlayer && score === null && currentDice.length > 0 ? styles.scoreCellActive : null]}
                    onPress={() => isCurrentPlayer && score === null && currentDice.length > 0 ? scoreCategory(category.key as ScoreCategory) : null}
                    disabled={!isCurrentPlayer || score !== null || currentDice.length === 0}
                  >
                    <Text style={[styles.scoreValue, potential !== null ? styles.potentialScore : null]}>
                      {score !== null ? score : (potential !== null ? potential : '—')}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Upper total</Text>
            {['Player 1', 'Player 2', 'Botzee'].map(player => {
              const upperTotal = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              return (
                <View key={player} style={styles.scoreCell}>
                  <Text style={styles.scoreValue}>{upperTotal}</Text>
                </View>
              );
            })}
          </View>

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Bonus (+35)</Text>
            {['Player 1', 'Player 2', 'Botzee'].map(player => {
              const upperTotal = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              const bonus = upperTotal >= 63 ? 35 : 0;
              return (
                <View key={player} style={styles.scoreCell}>
                  <Text style={styles.scoreValue}>{bonus}</Text>
                </View>
              );
            })}
          </View>

          {/* Lower Section */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>LOWER SECTION</Text>
          </View>

          {[{name: 'Three of a Kind', key: 'threeOfAKind'}, {name: 'Four of a Kind', key: 'fourOfAKind'}, 
            {name: 'Full House', key: 'fullHouse'}, {name: 'Small Straight', key: 'smallStraight'}, 
            {name: 'Large Straight', key: 'largeStraight'}, {name: 'Yahtzee', key: 'yahtzee'}, 
            {name: 'Chance', key: 'chance'}].map((category) => (
            <View key={category.key} style={styles.scorecardRow}>
              <Text style={styles.categoryName}>{category.name}</Text>
              {['Player 1', 'Player 2', 'Botzee'].map(player => {
                const score = scores[player][category.key as ScoreCategory];
                const isCurrentPlayer = player === currentPlayer;
                const potential = isCurrentPlayer && currentDice.length > 0 && score === null ? getPotentialScore(category.key as ScoreCategory) : null;
                
                return (
                  <TouchableOpacity 
                    key={player}
                    style={[styles.scoreCell, isCurrentPlayer && score === null && currentDice.length > 0 ? styles.scoreCellActive : null]}
                    onPress={() => isCurrentPlayer && score === null && currentDice.length > 0 ? scoreCategory(category.key as ScoreCategory) : null}
                    disabled={!isCurrentPlayer || score !== null || currentDice.length === 0}
                  >
                    <Text style={[styles.scoreValue, potential !== null ? styles.potentialScore : null]}>
                      {score !== null ? score : (potential !== null ? potential : '—')}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Yahtzee Bonus</Text>
            {['Player 1', 'Player 2', 'Botzee'].map(player => (
              <View key={player} style={styles.scoreCell}>
                <Text style={styles.scoreValue}>0</Text>
              </View>
            ))}
          </View>

          <View style={[styles.scorecardRow, styles.totalRow, styles.grandTotalRow]}>
            <Text style={[styles.categoryName, styles.grandTotalText]}>GRAND TOTAL</Text>
            {['Player 1', 'Player 2', 'Botzee'].map(player => {
              const upperTotal = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              const upperBonus = upperTotal >= 63 ? 35 : 0;
              const lowerTotal = ['threeOfAKind', 'fourOfAKind', 'fullHouse', 'smallStraight', 'largeStraight', 'yahtzee', 'chance']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              const grandTotal = upperTotal + upperBonus + lowerTotal;
              
              return (
                <View key={player} style={styles.scoreCell}>
                  <Text style={[styles.scoreValue, styles.grandTotalText]}>{grandTotal}</Text>
                </View>
              );
            })}
          </View>
        </View>

        {/* Chat Section */}
        <View style={styles.chatContainer}>
          <Text style={styles.chatTitle}>💬 Chat with Botzee</Text>
          <ScrollView 
            ref={chatScrollRef}
            style={styles.chatMessages}
            showsVerticalScrollIndicator={false}
            onContentSizeChange={() => chatScrollRef.current?.scrollToEnd({ animated: true })}
          >
            {chatMessages.map((message) => (
              <Text key={message.id} style={[
                styles.chatMessage,
                message.sender === 'player' ? styles.playerMessage : styles.botzeeMessage
              ]}>
                {message.sender === 'botzee' ? 'Botzee: ' : 'You: '}{message.text}
              </Text>
            ))}
          </ScrollView>
          <View style={styles.chatInputContainer}>
            <TextInput
              style={styles.chatInput}
              placeholder="Ask Botzee..."
              value={chatInput}
              onChangeText={setChatInput}
              onSubmitEditing={sendMessage}
              returnKeyType="send"
            />
            <TouchableOpacity 
              style={styles.sendButton}
              onPress={sendMessage}
            >
              <Text style={styles.sendButtonText}>Send</Text>
            </TouchableOpacity>
          </View>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a', // Dark background like the image
  },
  scrollView: {
    backgroundColor: '#1a1a1a',
    padding: 16,
  },
  
  // Turn Info Section
  turnInfo: {
    backgroundColor: '#2a2a2a',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  turnInfoText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
    flex: 1,
    textAlign: 'center',
  },
  rollButton: {
    backgroundColor: '#e74c3c',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    flex: 1,
    alignItems: 'center',
    marginHorizontal: 8,
  },
  rollButtonDisabled: {
    backgroundColor: '#666666',
  },

  // Dice Section
  diceContainer: {
    backgroundColor: '#2a2a2a',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  diceGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  die: {
    width: 50,
    height: 50,
    borderWidth: 3,
    borderColor: '#ffffff',
    borderRadius: 8,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  dieEmpty: {
    borderColor: '#666666',
    backgroundColor: '#3a3a3a',
  },
  dieSelected: {
    borderColor: '#27ae60',
    backgroundColor: '#e8f5e8',
  },
  dieText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#000000',
  },
  dieTextEmpty: {
    color: '#666666',
  },

  // Scorecard Section
  scorecard: {
    backgroundColor: '#2a2a2a',
    borderRadius: 12,
    marginBottom: 16,
    overflow: 'hidden',
  },
  scorecardHeader: {
    backgroundColor: '#3a3a3a',
    paddingVertical: 12,
  },
  scorecardRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#444444',
  },
  scorecardHeaderText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 12,
    flex: 2,
  },
  scorecardHeaderCenter: {
    flex: 1,
    textAlign: 'center',
  },
  sectionHeader: {
    backgroundColor: '#3a3a3a',
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  sectionTitle: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  categoryName: {
    color: '#ffffff',
    fontSize: 14,
    flex: 2,
  },
  scoreCell: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 4,
  },
  scoreCellActive: {
    backgroundColor: '#2a2a2a',
    borderRadius: 4,
  },
  scoreValue: {
    color: '#ffffff',
    fontSize: 14,
    textAlign: 'center',
  },
  potentialScore: {
    color: '#3498db',
    fontStyle: 'italic',
  },
  totalRow: {
    backgroundColor: '#3a3a3a',
  },
  grandTotalRow: {
    backgroundColor: '#4a4a4a',
    borderBottomWidth: 0,
  },
  grandTotalText: {
    fontWeight: 'bold',
    fontSize: 16,
  },

  // Chat Section
  chatContainer: {
    backgroundColor: '#2a2a2a',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  chatTitle: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 16,
    marginBottom: 12,
  },
  chatMessages: {
    backgroundColor: '#3a3a3a',
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    height: 84, // Fixed height for exactly 3 lines (20px line height + 4px margin = 24px per line, plus padding)
    maxHeight: 84,
  },
  chatMessage: {
    color: '#ffffff',
    fontSize: 14,
    marginBottom: 4,
    lineHeight: 20,
  },
  playerMessage: {
    textAlign: 'right',
    color: '#3498db',
  },
  botzeeMessage: {
    textAlign: 'left',
    fontStyle: 'italic',
  },
  chatInputContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  chatInput: {
    flex: 1,
    backgroundColor: '#3a3a3a',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 8,
    color: '#ffffff',
    fontSize: 14,
  },
  sendButton: {
    backgroundColor: '#3498db',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    justifyContent: 'center',
  },
  sendButtonText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 14,
  },
});

export default App;