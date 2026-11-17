Feature: Petrol-car fee boundaries
  As a registered ParkEase driver
  I want parking charges to follow the published time bands
  So that the amount taken from my wallet is predictable

  Background:
    Given driver "Usman" has an active ParkEase session
    And the petrol vehicle "ISB-9012" belongs to this driver
    And the wallet contains Rs. 1,000

  @boundary
  Scenario Outline: Petrol parking duration produces the stated charge
    Given the vehicle has stayed for <duration>
    When the vehicle exits the plaza
    Then the parking fee should be <fee>
    And the service fee should be <service>
    And the total charge should be <total>
    And the remaining wallet should be <balance>
    And the exit barrier should open

    Examples: Free and rounding
      | duration   | fee     | service | total   | balance   |
      | 15 min 0 s | Rs. 0   | Rs. 0   | Rs. 0   | Rs. 1,000 |
      | 15 min 1 s | Rs. 100 | Rs. 20  | Rs. 120 | Rs. 880   |
      | 60 min 0 s | Rs. 100 | Rs. 20  | Rs. 120 | Rs. 880   |
      | 61 min 0 s | Rs. 160 | Rs. 20  | Rs. 180 | Rs. 820   |

    Examples: Daily cap
      | duration       | fee     | service | total   | balance |
      | 12 h 0 min 0 s | Rs. 760 | Rs. 20  | Rs. 780 | Rs. 220 |
      | 12 h 0 min 1 s | Rs. 800 | Rs. 20  | Rs. 820 | Rs. 180 |
      | 30 h 0 min 0 s | Rs. 800 | Rs. 20  | Rs. 820 | Rs. 180 |
