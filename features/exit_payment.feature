Feature: Automatic ParkEase wallet settlement
  As a registered ParkEase driver
  I want the parking amount to be collected from my wallet when leaving
  So that I can exit the parking plaza without waiting at a cashier

  @smoke
  Scenario: An electric-car driver completes a normal exit payment
    Given driver "Sara" has an active ParkEase session
    And the electric vehicle "ICT-4521" belongs to this driver
    And the wallet contains Rs. 1,000
    And the vehicle entered at 09:00
    When the vehicle exits at 12:40
    Then the driver should receive the message "Payment successful – gate opening"
    And the parking fee should be Rs. 280
    And the EV reduction should be Rs. 70
    And the service fee should be Rs. 20
    And the total charge should be Rs. 230
    And the remaining wallet should be Rs. 770
    And the exit barrier should open

  @boundary
  Scenario: Electric-car discount is calculated from the capped fee
    Given driver "Hassan" has an active ParkEase session
    And the electric vehicle "RWL-7788" belongs to this driver
    And the wallet contains Rs. 1,000
    And the vehicle has stayed for 20 h 0 min
    When the vehicle exits the plaza
    Then the driver should receive the message "Payment successful – gate opening"
    And the parking fee should be Rs. 800
    And the EV reduction should be Rs. 200
    And the service fee should be Rs. 20
    And the total charge should be Rs. 620
    And the remaining wallet should be Rs. 380
    And the exit barrier should open
