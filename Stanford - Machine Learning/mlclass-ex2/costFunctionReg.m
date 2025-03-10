function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples
numFeatures = length(theta); % number of features

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

% the cost function in vectorization form
J = - 1 / m * sum(y' * log(sigmoid(X * theta)) .+ (1 - y)' * log(1 - sigmoid(X * theta))) + lambda / (2 * m) * (theta' * theta - theta(1,1) * theta(1,1));

% compute the derivative(which is the gradient descent, the slope)
for i = 1:numFeatures,
	if(i == 1)
		grad(i,1) = 1 / m * (sum((sigmoid(X * theta) - y) .* X(:,i)));
	else
		grad(i,1) = 1 / m * (sum((sigmoid(X * theta) - y) .* X(:,i)) + lambda * theta(i,1));
	endif
end;




% =============================================================

end
