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

// Game state management
const App = () => {
  const [currentPlayer, setCurrentPlayer] = useState('Player 1');
  const [rollsLeft, setRollsLeft] = useState(3);
  const [currentDice, setCurrentDice] = useState<number[]>([]);
  const [selectedDice, setSelectedDice] = useState<number[]>([]);
  const [gameStarted, setGameStarted] = useState(false);
  const [chatInput, setChatInput] = useState('');

  // Mock scorecard data - in real app, this would come from backend
  const mockScores = {
    'Player 1': { ones: null, twos: null, threes: null },
    'Player 2': { ones: null, twos: null, threes: null },
    'Botzee': { ones: null, twos: null, threes: null }
  };

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

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#ffffff" />
      <ScrollView style={styles.scrollView}>
        
        {/* Turn Info */}
        <View style={styles.turnInfo}>
          <Text style={styles.turnPlayer}>🎯 {currentPlayer}</Text>
          <View style={styles.rollsContainer}>
            <Text style={styles.rollsText}>Rolls left: {rollsLeft}</Text>
            <TouchableOpacity 
              style={[styles.rollButton, !gameStarted || rollsLeft === 0 ? styles.rollButtonDisabled : null]}
              onPress={gameStarted ? rerollDice : rollDice}
              disabled={rollsLeft === 0}
            >
              <Text style={styles.rollButtonText}>
                {!gameStarted ? '🎲 Roll Dice' : rollsLeft > 0 ? '🎲 Next Roll' : '🎲 No Rolls Left'}
              </Text>
            </TouchableOpacity>
          </View>
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
              <Text style={styles.scorecardHeaderText}>Category</Text>
              <Text style={styles.scorecardHeaderText}>🎯 Player 1</Text>
              <Text style={styles.scorecardHeaderText}>Player 2</Text>
              <Text style={styles.scorecardHeaderText}>Botzee</Text>
            </View>
          </View>

          {/* Upper Section */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>UPPER SECTION</Text>
          </View>
          
          {['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes'].map((category) => (
            <View key={category} style={styles.scorecardRow}>
              <Text style={styles.categoryName}>{category}</Text>
              <Text style={styles.scoreValue}>0</Text>
              <Text style={styles.scoreValue}>0</Text>
              <Text style={styles.scoreValue}>0</Text>
            </View>
          ))}

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Upper total</Text>
            <Text style={styles.scoreValue}>0</Text>
            <Text style={styles.scoreValue}>0</Text>
            <Text style={styles.scoreValue}>0</Text>
          </View>

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Bonus (+35)</Text>
            <Text style={styles.scoreValue}>0</Text>
            <Text style={styles.scoreValue}>0</Text>
            <Text style={styles.scoreValue}>0</Text>
          </View>

          {/* Lower Section */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>LOWER SECTION</Text>
          </View>

          {['Three of a Kind', 'Four of a Kind', 'Full House', 'Small Straight', 'Large Straight', 'Yahtzee', 'Chance'].map((category) => (
            <View key={category} style={styles.scorecardRow}>
              <Text style={styles.categoryName}>{category}</Text>
              <Text style={styles.scoreValue}>0</Text>
              <Text style={styles.scoreValue}>0</Text>
              <Text style={styles.scoreValue}>0</Text>
            </View>
          ))}

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Yahtzee Bonus</Text>
            <Text style={styles.scoreValue}>0</Text>
            <Text style={styles.scoreValue}>0</Text>
            <Text style={styles.scoreValue}>0</Text>
          </View>

          <View style={[styles.scorecardRow, styles.totalRow, styles.grandTotalRow]}>
            <Text style={[styles.categoryName, styles.grandTotalText]}>GRAND TOTAL</Text>
            <Text style={[styles.scoreValue, styles.grandTotalText]}>0</Text>
            <Text style={[styles.scoreValue, styles.grandTotalText]}>0</Text>
            <Text style={[styles.scoreValue, styles.grandTotalText]}>0</Text>
          </View>
        </View>

        {/* Chat Section */}
        <View style={styles.chatContainer}>
          <Text style={styles.chatTitle}>💬 Chat with Botzee</Text>
          <View style={styles.chatMessages}>
            <Text style={styles.chatMessage}>Botzee: Ready to play! Tap 'Roll Dice' to start.</Text>
          </View>
          <View style={styles.chatInputContainer}>
            <TextInput
              style={styles.chatInput}
              placeholder="Ask Botzee..."
              value={chatInput}
              onChangeText={setChatInput}
            />
            <TouchableOpacity style={styles.sendButton}>
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
  turnPlayer: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#e74c3c',
  },
  rollsContainer: {
    alignItems: 'flex-end',
  },
  rollsText: {
    color: '#ffffff',
    fontSize: 14,
    marginBottom: 8,
  },
  rollButton: {
    backgroundColor: '#e74c3c',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  rollButtonDisabled: {
    backgroundColor: '#666666',
  },
  rollButtonText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 14,
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
    justifyContent: 'space-between',
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
  scoreValue: {
    color: '#ffffff',
    fontSize: 14,
    flex: 1,
    textAlign: 'center',
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
    minHeight: 60,
  },
  chatMessage: {
    color: '#ffffff',
    fontSize: 14,
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