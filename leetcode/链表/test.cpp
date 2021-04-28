/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode* L;
        ListNode* L = new ListNode(-1);
        int carry = 0; int newval = 0;
        while(l1 != nullptr || l2 != nullptr || carry>0)
        {
            newval = (l1 == nullptr ? 0:l1->val) + (l2 == nullptr ?0:l2->val) + carry;
            carry = newval/10;
            newval %= 10;
            L->next = new ListNode(newval);
            l1 == nullptr ? nullptr:l1->next;
            l2 == nullptr ? nullptr: l2->next;
            L = L->next;
        }
        return L->next;
        }
    }
};