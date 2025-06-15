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
  FlatList,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useRef } from 'react';
import { useFonts, PressStart2P_400Regular } from '@expo-google-fonts/press-start-2p';
import * as SplashScreen from 'expo-splash-screen';

SplashScreen.preventAutoHideAsync();

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
  let [fontsLoaded] = useFonts({
    PressStart2P_400Regular,
  });

  const [currentPlayer, setCurrentPlayer] = useState('Player 1');
  const [rollsLeft, setRollsLeft] = useState(3);
  const [currentDice, setCurrentDice] = useState<number[]>([]);
  const [selectedDice, setSelectedDice] = useState<number[]>([]);
  const [gameStarted, setGameStarted] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [showChat, setShowChat] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'botzee',
      text: 'Ready to play! Tap \'Roll Dice\' to start.',
      timestamp: new Date()
    }
  ]);
  const chatInputRef = useRef<TextInput>(null);
  const flatListRef = useRef<FlatList>(null);

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
      flatListRef.current?.scrollToEnd({ animated: true });
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
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }, 500);
  };

  const openChat = () => {
    setShowChat(true);
    setTimeout(() => {
      chatInputRef.current?.focus();
    }, 100);
  };

  const closeChat = () => {
    setShowChat(false);
    setChatInput('');
  };

  const renderChatMessage = ({ item }: { item: ChatMessage }) => (
    <View style={styles.messageContainer}>
      <Text style={[
        styles.chatMessage,
        item.sender === 'player' ? styles.playerMessage : styles.botzeeMessage
      ]}>
        {item.sender === 'botzee' ? 'Botzee: ' : 'You: '}{item.text}
      </Text>
    </View>
  );

  if (!fontsLoaded) {
    return null;
  } else {
    SplashScreen.hideAsync();
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#e4e1b4" />
      <ScrollView style={styles.scrollView}>
        
        {/* Action Section (Top) */}
        <View style={styles.actionSection}>
          {/* Overlay for score selection */}
          {rollsLeft === 0 && currentDice.length > 0 && (
            <View style={styles.scoreOverlay}>
              <Text style={styles.scoreOverlayText}>{currentPlayer}, choose your score!</Text>
            </View>
          )}
          {/* Top Row: Player Info and Roll Button */}
          <View style={styles.playerInfo}>
            <Text style={styles.playerInfoText}>{currentPlayer}</Text>
            <TouchableOpacity 
              style={[styles.rollButton, !gameStarted || rollsLeft === 0 ? styles.rollButtonDisabled : null]}
              onPress={gameStarted ? rerollDice : rollDice}
              disabled={rollsLeft === 0}
            >
              <Text style={styles.rollButtonText}>
                {!gameStarted ? 'Roll' : rollsLeft > 0 ? 'Roll' : 'Choose Score'}
              </Text>
            </TouchableOpacity>
            <Text style={styles.playerInfoText}>Rolls: {rollsLeft}</Text>
          </View>
          
          {/* Dice Grid */}
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

        {/* Scorecard Section (Middle) */}
        <View style={styles.scorecard}>
          {/* Combined Header: Player Names and Upper Section */}
          <View style={styles.combinedHeader}>
            <Text style={styles.sectionTitle}>Upper{"\n"}Section</Text>
            <View style={styles.playerNamesRow}>
              <View style={[styles.playerNameContainer, currentPlayer === 'Player 1' ? styles.currentPlayerName : null]}>
                <Text style={[styles.scorecardHeaderText, styles.scorecardHeaderCenter]}>P1</Text>
              </View>
              <View style={[styles.playerNameContainer, currentPlayer === 'Player 2' ? styles.currentPlayerName : null]}>
                <Text style={[styles.scorecardHeaderText, styles.scorecardHeaderCenter]}>P2</Text>
              </View>
              <View style={[styles.playerNameContainer, currentPlayer === 'Botzee' ? styles.currentPlayerName : null]}>
                <Text style={[styles.scorecardHeaderText, styles.scorecardHeaderCenter]}>BOT</Text>
              </View>
            </View>
          </View>
          
          {[{name: 'Ones', key: 'ones'}, {name: 'Twos', key: 'twos'}, {name: 'Threes', key: 'threes'}, 
            {name: 'Fours', key: 'fours'}, {name: 'Fives', key: 'fives'}, {name: 'Sixes', key: 'sixes'}].map((category) => (
            <View key={category.key} style={styles.scorecardRow}>
              <Text style={styles.categoryName}>{category.name}</Text>
              {['Player 1', 'Player 2', 'Botzee'].map((player, index) => {
                const score = scores[player][category.key as ScoreCategory];
                const isCurrentPlayer = player === currentPlayer;
                const potential = isCurrentPlayer && currentDice.length > 0 && score === null ? getPotentialScore(category.key as ScoreCategory) : null;
                
                return (
                  <TouchableOpacity 
                    key={player}
                    style={[styles.scoreCell, index === 0 ? styles.firstScoreCell : null, index < 2 ? styles.scoreCellWithBorder : null]}
                    onPress={() => isCurrentPlayer && score === null && currentDice.length > 0 ? scoreCategory(category.key as ScoreCategory) : null}
                    disabled={!isCurrentPlayer || score !== null || currentDice.length === 0}
                  >
                    <Text style={[styles.scoreValue, potential !== null ? styles.potentialScore : null, score !== null ? styles.actualScore : null]}>
                      {score !== null ? score : (potential !== null ? potential : '—')}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Upper Total</Text>
            {['Player 1', 'Player 2', 'Botzee'].map((player, index) => {
              const upperTotal = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              return (
                <View key={player} style={[styles.scoreCell, index === 0 ? styles.firstScoreCell : null, index < 2 ? styles.scoreCellWithBorder : null]}>
                  <Text style={[styles.scoreValue, styles.actualScore]}>{upperTotal}</Text>
                </View>
              );
            })}
          </View>

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Bonus</Text>
            {['Player 1', 'Player 2', 'Botzee'].map((player, index) => {
              const upperTotal = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              const bonus = upperTotal >= 63 ? 35 : 0;
              return (
                <View key={player} style={[styles.scoreCell, index === 0 ? styles.firstScoreCell : null, index < 2 ? styles.scoreCellWithBorder : null]}>
                  <Text style={[styles.scoreValue, styles.actualScore]}>{bonus}</Text>
                </View>
              );
            })}
          </View>

          {/* Lower Section */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Lower{"\n"}Section</Text>
          </View>

          {[{name: 'Three of a Kind', key: 'threeOfAKind'}, {name: 'Four of a Kind', key: 'fourOfAKind'}, 
            {name: 'Full House', key: 'fullHouse'}, {name: 'Small Straight', key: 'smallStraight'}, 
            {name: 'Large Straight', key: 'largeStraight'}, {name: 'Yahtzee', key: 'yahtzee'}, 
            {name: 'Chance', key: 'chance'}].map((category) => (
            <View key={category.key} style={styles.scorecardRow}>
              <Text style={styles.categoryName}>{category.name}</Text>
              {['Player 1', 'Player 2', 'Botzee'].map((player, index) => {
                const score = scores[player][category.key as ScoreCategory];
                const isCurrentPlayer = player === currentPlayer;
                const potential = isCurrentPlayer && currentDice.length > 0 && score === null ? getPotentialScore(category.key as ScoreCategory) : null;
                
                return (
                  <TouchableOpacity 
                    key={player}
                    style={[styles.scoreCell, index === 0 ? styles.firstScoreCell : null, index < 2 ? styles.scoreCellWithBorder : null]}
                    onPress={() => isCurrentPlayer && score === null && currentDice.length > 0 ? scoreCategory(category.key as ScoreCategory) : null}
                    disabled={!isCurrentPlayer || score !== null || currentDice.length === 0}
                  >
                    <Text style={[styles.scoreValue, potential !== null ? styles.potentialScore : null, score !== null ? styles.actualScore : null]}>
                      {score !== null ? score : (potential !== null ? potential : '—')}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}

          <View style={[styles.scorecardRow, styles.totalRow]}>
            <Text style={styles.categoryName}>Yahtzee Bonus</Text>
            {['Player 1', 'Player 2', 'Botzee'].map((player, index) => (
              <View key={player} style={[styles.scoreCell, index === 0 ? styles.firstScoreCell : null]}>
                <Text style={[styles.scoreValue, styles.actualScore]}>0</Text>
              </View>
            ))}
          </View>

          <View style={[styles.scorecardRow, styles.totalRow, styles.grandTotalRow]}>
            <Text style={[styles.categoryName, styles.grandTotalText]}>Grand Total</Text>
            {['Player 1', 'Player 2', 'Botzee'].map((player, index) => {
              const upperTotal = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              const upperBonus = upperTotal >= 63 ? 35 : 0;
              const lowerTotal = ['threeOfAKind', 'fourOfAKind', 'fullHouse', 'smallStraight', 'largeStraight', 'yahtzee', 'chance']
                .reduce((total, cat) => total + (scores[player][cat as ScoreCategory] || 0), 0);
              const grandTotal = upperTotal + upperBonus + lowerTotal;
              
              return (
                <View key={player} style={[styles.scoreCell, index === 0 ? styles.firstScoreCell : null, index < 2 ? styles.scoreCellWithBorder : null]}>
                  <Text style={[styles.scoreValue, styles.grandTotalText, styles.actualScore]}>{grandTotal}</Text>
                </View>
              );
            })}
          </View>
        </View>

        {/* Chat Button (Bottom) */}
        {!showChat && (
          <TouchableOpacity style={styles.chatButton} onPress={openChat}>
            <Text style={styles.chatButtonText}>Chat with Botzee!</Text>
          </TouchableOpacity>
        )}

      </ScrollView>

      {/* Full Screen Chat Window */}
      {showChat && (
        <KeyboardAvoidingView 
          style={styles.chatOverlay}
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
        >
          <View style={styles.chatWindow}>
            <View style={styles.chatHeader}>
              <Text style={styles.chatHeaderTitle}>Chat with Botzee</Text>
              <TouchableOpacity style={styles.closeButton} onPress={closeChat}>
                <Text style={styles.closeButtonText}>×</Text>
              </TouchableOpacity>
            </View>
            
            <FlatList
              ref={flatListRef}
              data={chatMessages}
              renderItem={renderChatMessage}
              keyExtractor={(item) => item.id}
              style={styles.chatMessagesList}
              contentContainerStyle={styles.chatMessagesContent}
              showsVerticalScrollIndicator={false}
              onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
            />
            
            <View style={styles.chatInputContainer}>
              <TextInput
                ref={chatInputRef}
                style={styles.chatInput}
                placeholder="Ask Botzee..."
                placeholderTextColor="#666666"
                value={chatInput}
                onChangeText={setChatInput}
                onSubmitEditing={sendMessage}
                returnKeyType="send"
                multiline={false}
              />
              <TouchableOpacity 
                style={styles.sendButton}
                onPress={sendMessage}
              >
                <Text style={styles.sendButtonText}>Send</Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#e4e1b4', // Game Boy yellow-green background
    maxWidth: 2556, // iPhone 15 width
    maxHeight: 1179, // iPhone 15 height
    alignSelf: 'center',
  },
  scrollView: {
    backgroundColor: '#e4e1b4',
    padding: 8,
  },
  
  // Action Section (Top)
  actionSection: {
    backgroundColor: '#e4e1b4',
    borderWidth: 3,
    borderColor: '#000000',
    padding: 12,
    marginBottom: 6,
  },
  playerInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  playerInfoText: {
    color: '#000000',
    fontSize: 16,
    fontFamily: 'PressStart2P_400Regular',
  },
  rollButton: {
    backgroundColor: '#ff0000',
    borderWidth: 3,
    borderColor: '#000000',
    paddingHorizontal: 12,
    paddingVertical: 6,
    alignSelf: 'center',
  },
  rollButtonDisabled: {
    backgroundColor: '#666666',
  },
  rollButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontFamily: 'PressStart2P_400Regular',
  },

  // Dice Section
  diceContainer: {
    backgroundColor: '#e4e1b4',
    borderWidth: 3,
    borderColor: '#000000',
    padding: 8,
    marginBottom: 6,
  },
  diceGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  die: {
    width: 70,
    height: 70,
    borderWidth: 3,
    borderColor: '#000000',
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  dieEmpty: {
    backgroundColor: '#cccccc',
  },
  dieSelected: {
    backgroundColor: '#ffff00',
  },
  dieText: {
    fontSize: 28,
    color: '#000000',
    fontFamily: 'PressStart2P_400Regular',
  },
  dieTextEmpty: {
    color: '#666666',
  },

  // Scorecard Section (Middle)
  scorecard: {
    backgroundColor: '#e4e1b4',
    borderWidth: 3,
    borderColor: '#000000',
    marginBottom: 8,
  },
  scorecardHeader: {
    backgroundColor: '#e4e1b4',
    paddingVertical: 4,
  },
  scorecardRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderBottomWidth: 2,
    borderBottomColor: '#000000',
    backgroundColor: '#e4e1b4',
  },
  scorecardHeaderText: {
    color: '#000000',
    fontSize: 14,
    fontFamily: 'PressStart2P_400Regular',
  },
  scorecardHeaderCenter: {
    textAlign: 'center',
  },
  combinedHeader: {
    backgroundColor: '#e4e1b4',
    borderBottomWidth: 3,
    borderBottomColor: '#000000',
    paddingVertical: 6,
    paddingHorizontal: 12,
    flexDirection: 'row',
    alignItems: 'center',
  },
  playerNamesRow: {
    flex: 3,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  sectionHeader: {
    backgroundColor: '#e4e1b4',
    borderBottomWidth: 2,
    borderBottomColor: '#000000',
    paddingVertical: 2,
    paddingHorizontal: 6,
  },
  sectionTitle: {
    color: '#000000',
    fontSize: 14,
    fontFamily: 'PressStart2P_400Regular',
    flex: 2,
    textAlign: 'left',
  },
  categoryName: {
    color: '#000000',
    fontSize: 12,
    fontFamily: 'PressStart2P_400Regular',
    flex: 2,
  },
  scoreCell: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 4,
  },
  scoreCellWithBorder: {
    borderRightWidth: 3,
    borderRightColor: '#000000',
  },
  firstScoreCell: {
    borderLeftWidth: 3,
    borderLeftColor: '#000000',
  },
  scoreCellActive: {
    backgroundColor: '#e4e1b4',
  },
  scoreValue: {
    color: '#000000',
    fontSize: 12,
    fontFamily: 'PressStart2P_400Regular',
    textAlign: 'center',
  },
  potentialScore: {
    color: '#000000',
    fontStyle: 'italic',
  },
  actualScore: {
    fontWeight: 'bold',
  },
  totalRow: {
    backgroundColor: '#cccccc',
  },
  grandTotalRow: {
    backgroundColor: '#aaaaaa',
    borderBottomWidth: 0,
  },
  grandTotalText: {
    fontSize: 12,
    fontFamily: 'PressStart2P_400Regular',
  },
  
  // Score overlay styles
  scoreOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 40,
    backgroundColor: 'rgba(255, 0, 0, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
    borderBottomWidth: 3,
    borderBottomColor: '#000000',
  },
  scoreOverlayText: {
    color: '#ffffff',
    fontSize: 14,
    fontFamily: 'PressStart2P_400Regular',
  },
  
  // Player name highlight styles
  playerNameContainer: {
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  currentPlayerName: {
    borderWidth: 2,
    borderColor: '#ff0000',
    backgroundColor: 'rgba(255, 0, 0, 0.1)',
  },

  // Chat Button (Bottom)
  chatButton: {
    backgroundColor: '#00ff00',
    borderWidth: 3,
    borderColor: '#000000',
    padding: 16,
    marginBottom: 8,
    alignItems: 'center',
  },
  chatButtonText: {
    color: '#000000',
    fontSize: 16,
    fontFamily: 'PressStart2P_400Regular',
  },

  // Full Screen Chat Window
  chatOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    justifyContent: 'flex-end',
  },
  chatWindow: {
    backgroundColor: '#e4e1b4',
    borderTopWidth: 3,
    borderTopColor: '#000000',
    height: '80%',
    paddingTop: 0,
  },
  chatHeader: {
    backgroundColor: '#e4e1b4',
    borderBottomWidth: 3,
    borderBottomColor: '#000000',
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  chatHeaderTitle: {
    color: '#000000',
    fontSize: 16,
    fontFamily: 'PressStart2P_400Regular',
  },
  closeButton: {
    backgroundColor: '#ff0000',
    borderWidth: 2,
    borderColor: '#000000',
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    color: '#ffffff',
    fontSize: 20,
    fontFamily: 'PressStart2P_400Regular',
    lineHeight: 20,
  },
  chatMessagesList: {
    flex: 1,
    backgroundColor: '#ffffff',
    marginHorizontal: 12,
    marginTop: 12,
    borderWidth: 2,
    borderColor: '#000000',
  },
  chatMessagesContent: {
    padding: 12,
  },
  messageContainer: {
    marginVertical: 4,
  },
  chatMessage: {
    color: '#000000',
    fontSize: 14,
    fontFamily: 'PressStart2P_400Regular',
    lineHeight: 20,
  },
  playerMessage: {
    textAlign: 'right',
    color: '#0066cc',
  },
  botzeeMessage: {
    textAlign: 'left',
    color: '#cc6600',
  },
  chatInputContainer: {
    flexDirection: 'row',
    padding: 12,
    gap: 12,
    backgroundColor: '#e4e1b4',
  },
  chatInput: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderWidth: 3,
    borderColor: '#000000',
    paddingHorizontal: 12,
    paddingVertical: 8,
    color: '#000000',
    fontSize: 14,
    fontFamily: 'PressStart2P_400Regular',
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#ff0000',
    borderWidth: 3,
    borderColor: '#000000',
    paddingHorizontal: 16,
    paddingVertical: 8,
    justifyContent: 'center',
  },
  sendButtonText: {
    color: '#ffffff',
    fontSize: 12,
    fontFamily: 'PressStart2P_400Regular',
  },
});

export default App;