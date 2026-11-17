Feature: Refuse exit when the wallet cannot cover the payment
  As a ParkEase driver
  I want an unpaid exit to be stopped
  So that a vehicle cannot leave before its parking charge is settled

  @negative
  Scenario: Exit is refused when the wallet is one rupee short
    Given driver "Usman" has an active ParkEase session
    And the petrol vehicle "ISB-9012" belongs to this driver
    And the wallet contains Rs. 239
    And the vehicle entered at 10:00
    When the vehicle exits at 12:10
    Then the driver should receive the message "Insufficient wallet balance"
    And the wallet amount should remain unchanged
    And the remaining wallet should be Rs. 239
    And the exit barrier should remain closed
