package DecisionTree


import Constraints.CstDummyEnd
import DataManipulation.Data
import oscar.cp.core.CPStore
import oscar.cp.core.variables.CPIntVar

class DEndNode(
                solver: CPStore,
                leftChild: DLeaf,
                rightChild: DLeaf,
                db: Data,
                id: Int
              )
  extends DTreeDecision(1, solver, db, id, leftChild, rightChild) {

  /**
    * Tree Structure
    */
  lazy val subProblems : Seq[DTreeDecision] = Seq()

  def getFirstChild: Option[DTreeDecision] = None

  val belowDecisionDFS: Array[CPIntVar] = Array(decision)
  val belowProblemDFS: Array[DTreeDecision] = Array(this)

  /**
    * Apply Functions
    */
  def applyToAllNode(fct: DTreeDecision => Unit): Unit = fct(this)

  def applyToNode(fct: DNode => Unit): Unit = {}

  def applyToEndNode(fct: DEndNode => Unit): Unit = fct(this)

  def applyToLeaf(fct: DLeaf => Unit): Unit = {
    leftChild.applyToLeaf(fct)
    rightChild.applyToLeaf(fct)
  }

  /**
    * Constraints
    */
  // Dummy
  def _addCstDummy: Unit =
    solver.add(new CstDummyEnd(decision, leftChild.countSum, rightChild.countSum))

  /**
    * TODO Rm?
    */
  def fillBFSAllNode[T](fct: DTreeDecision => T, array: Array[T], spot: Int): Unit =
    array(spot) = fct(this)
}
