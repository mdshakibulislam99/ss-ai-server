<?php
/**
 * API Client for communicating with the AI Server.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api;

use SS_AI_Image_Search\Api\Authentication;
use SS_AI_Image_Search\Api\Response;
use SS_AI_Image_Search\Api\ExceptionHandler;
use SS_AI_Image_Search\Exceptions\Api\ApiException;
use SS_AI_Image_Search\Exceptions\Api\TimeoutException;
use SS_AI_Image_Search\Exceptions\Api\ConnectionException;
use SS_AI_Image_Search\Exceptions\Api\ServerException;
use SS_AI_Image_Search\Exceptions\Api\RateLimitException;

/**
 * Client class for making HTTP requests to the AI Server.
 *
 * This is the ONLY class that should call WordPress HTTP API functions.
 * All other classes must use this Client to make HTTP requests.
 */
class Client {

	/**
	 * AI Server base URL.
	 *
	 * @var string
	 */
	private string $base_url;

	/**
	 * Request timeout in seconds.
	 *
	 * @var int
	 */
	private int $timeout;

	/**
	 * Connection timeout in seconds.
	 *
	 * @var int
	 */
	private int $connect_timeout;

	/**
	 * Maximum number of retries.
	 *
	 * @var int
	 */
	private int $max_retries;

	/**
	 * Authentication handler.
	 *
	 * @var Authentication
	 */
	private Authentication $authentication;

	/**
	 * Exception handler.
	 *
	 * @var ExceptionHandler
	 */
	private ExceptionHandler $exception_handler;

	/**
	 * Default request headers.
	 *
	 * @var array<string, string>
	 */
	private array $default_headers;

	/**
	 * Constructor.
	 *
	 * @param string              $base_url AI Server base URL.
	 * @param Authentication      $authentication Authentication handler.
	 * @param ExceptionHandler    $exception_handler Exception handler.
	 * @param array<string, int>  $config Configuration options.
	 */
	public function __construct(
		string $base_url,
		Authentication $authentication,
		ExceptionHandler $exception_handler,
		array $config = array()
	) {
		$this->base_url           = rtrim( $base_url, '/' );
		$this->authentication      = $authentication;
		$this->exception_handler   = $exception_handler;
		$this->timeout             = $config['timeout'] ?? 30;
		$this->connect_timeout     = $config['connect_timeout'] ?? 10;
		$this->max_retries         = $config['max_retries'] ?? 3;
		$this->default_headers     = $config['default_headers'] ?? array(
			'Content-Type' => 'application/json',
			'Accept'       => 'application/json',
		);
	}

	/**
	 * Make a GET request.
	 *
	 * @param string $endpoint API endpoint.
	 * @param array  $query_params Query parameters.
	 * @param array  $headers Additional headers.
	 * @return Response Response object.
	 * @throws ApiException If request fails after retries.
	 */
	public function get( string $endpoint, array $query_params = array(), array $headers = array() ): Response {
		$url = $this->build_url( $endpoint, $query_params );

		return $this->request_with_retry( 'GET', $url, array(), $headers );
	}

	/**
	 * Make a POST request.
	 *
	 * @param string $endpoint API endpoint.
	 * @param array  $data Request body data.
	 * @param array  $headers Additional headers.
	 * @return Response Response object.
	 * @throws ApiException If request fails after retries.
	 */
	public function post( string $endpoint, array $data = array(), array $headers = array() ): Response {
		$url = $this->build_url( $endpoint );

		$body = wp_json_encode( $data );

		return $this->request_with_retry( 'POST', $url, $body, $headers );
	}

	/**
	 * Make a PUT request.
	 *
	 * @param string $endpoint API endpoint.
	 * @param array  $data Request body data.
	 * @param array  $headers Additional headers.
	 * @return Response Response object.
	 * @throws ApiException If request fails after retries.
	 */
	public function put( string $endpoint, array $data = array(), array $headers = array() ): Response {
		$url = $this->build_url( $endpoint );

		$body = wp_json_encode( $data );

		return $this->request_with_retry( 'PUT', $url, $body, $headers );
	}

	/**
	 * Make a DELETE request.
	 *
	 * @param string $endpoint API endpoint.
	 * @param array  $query_params Query parameters.
	 * @param array  $headers Additional headers.
	 * @return Response Response object.
	 * @throws ApiException If request fails after retries.
	 */
	public function delete( string $endpoint, array $query_params = array(), array $headers = array() ): Response {
		$url = $this->build_url( $endpoint, $query_params );

		return $this->request_with_retry( 'DELETE', $url, array(), $headers );
	}

	/**
	 * Make a request with retry logic.
	 *
	 * @param string $method HTTP method.
	 * @param string $url Request URL.
	 * @param string|array $body Request body.
	 * @param array  $headers Additional headers.
	 * @return Response Response object.
	 * @throws ApiException If request fails after all retries.
	 */
	private function request_with_retry( string $method, string $url, $body = array(), array $headers = array() ): Response {
		$attempt       = 0;
		$last_exception = null;

		while ( $attempt <= $this->max_retries ) {
			try {
				return $this->make_request( $method, $url, $body, $headers );
			} catch ( \Throwable $exception ) {
				$last_exception = $exception;
				$attempt++;

				// Check if we should retry.
				if ( ! $this->exception_handler->should_retry( $exception ) || $attempt > $this->max_retries ) {
					break;
				}

				// Wait before retrying.
				$delay = $this->exception_handler->get_retry_delay( $exception, $attempt );
				sleep( $delay );
			}
		}

		// All retries failed, throw the last exception.
		if ( $last_exception instanceof ApiException ) {
			throw $last_exception;
		}

		// Convert generic exception to ConnectionException.
		throw new ConnectionException(
			sprintf( 'Request to %s failed after %d attempts: %s', $url, $attempt, $last_exception->getMessage() ),
			$last_exception->getCode(),
			array( 'url' => $url, 'attempts' => $attempt )
		);
	}

	/**
	 * Make a single HTTP request using WordPress HTTP API.
	 *
	 * @param string $method HTTP method.
	 * @param string $url Request URL.
	 * @param string|array $body Request body.
	 * @param array  $headers Additional headers.
	 * @return Response Response object.
	 * @throws ApiException If request fails.
	 */
	private function make_request( string $method, string $url, $body = array(), array $headers = array() ): Response {
		// Merge headers.
		$request_headers = array_merge( $this->default_headers, $this->authentication->get_headers(), $headers );

		// Build request arguments.
		$args = array(
			'method'      => $method,
			'headers'     => $request_headers,
			'timeout'     => $this->timeout,
			'redirection' => 0,
			'httpversion' => '1.1',
			'sslverify'   => true,
			'blocking'    => true,
			'data_format' => 'body',
		);

		// Add connection timeout.
		if ( function_exists( 'wp_remote_request' ) ) {
			$args['stream'] = false;
			$args['filename'] = null;
		}

		// Add body for POST/PUT requests.
		if ( in_array( strtoupper( $method ), array( 'POST', 'PUT', 'PATCH' ), true ) && ! empty( $body ) ) {
			$args['body'] = $body;
		}

		// Add query args for GET/DELETE.
		if ( in_array( strtoupper( $method ), array( 'GET', 'DELETE' ), true ) && is_array( $body ) && ! empty( $body ) ) {
			$args['body'] = $body;
		}

		// Make the request using WordPress HTTP API.
		$response = wp_remote_request( $url, $args );

		// Check for WordPress errors.
		if ( is_wp_error( $response ) ) {
			$error_message = $response->get_error_message();
			$error_code    = $response->get_error_code();

			// Determine exception type based on error.
			if ( strpos( $error_message, 'timed out' ) !== false || strpos( $error_message, 'timeout' ) !== false ) {
				throw new TimeoutException(
					sprintf( 'Request to %s timed out after %d seconds', $url, $this->timeout ),
					$error_code,
					array( 'url' => $url, 'timeout' => $this->timeout )
				);
			}

			if ( strpos( $error_message, 'Could not resolve host' ) !== false || strpos( $error_message, 'Connection refused' ) !== false ) {
				throw new ConnectionException(
					sprintf( 'Could not connect to %s: %s', $url, $error_message ),
					$error_code,
					array( 'url' => $url, 'error' => $error_message )
				);
			}

			throw new ConnectionException(
				sprintf( 'HTTP request failed: %s', $error_message ),
				$error_code,
				array( 'url' => $url, 'error' => $error_message )
			);
		}

		// Convert WordPress response to our Response object.
		$response_obj = Response::from_wp_response( $response );

		// Check for HTTP errors.
		if ( $response_obj->is_error() ) {
			$status_code = $response_obj->get_status_code();
			$message     = $response_obj->get_message();

			// Handle specific HTTP status codes.
			if ( 401 === $status_code ) {
				throw new \SS_AI_Image_Search\Exceptions\Api\AuthenticationException(
					$message ?: 'Authentication failed',
					$status_code,
					array( 'url' => $url )
				);
			}

			if ( 404 === $status_code ) {
				throw new \SS_AI_Image_Search\Exceptions\Api\NotFoundException(
					$message ?: 'Resource not found',
					$status_code,
					array( 'url' => $url )
				);
			}

			if ( 408 === $status_code ) {
				throw new TimeoutException(
					$message ?: 'Request timeout',
					$status_code,
					array( 'url' => $url, 'timeout' => $this->timeout )
				);
			}

			if ( 429 === $status_code ) {
				$retry_after = $response_obj->get_field( 'retry_after', 0 );
				throw new RateLimitException(
					$message ?: 'Rate limit exceeded',
					$status_code,
					array( 'url' => $url ),
					$retry_after
				);
			}

			if ( $status_code >= 500 ) {
				throw new ServerException(
					$message ?: 'Server error',
					$status_code,
					array( 'url' => $url )
				);
			}

			// Generic API exception for other errors.
			throw new ApiException(
				$message ?: 'Request failed',
				$status_code,
				array( 'url' => $url )
			);
		}

		return $response_obj;
	}

	/**
	 * Build full URL from endpoint.
	 *
	 * @param string $endpoint API endpoint.
	 * @param array  $query_params Query parameters.
	 * @return string Full URL.
	 */
	private function build_url( string $endpoint, array $query_params = array() ): string {
		$url = $this->base_url . '/' . ltrim( $endpoint, '/' );

		if ( ! empty( $query_params ) ) {
			$url = add_query_arg( $query_params, $url );
		}

		return $url;
	}

	/**
	 * Get the base URL.
	 *
	 * @return string Base URL.
	 */
	public function get_base_url(): string {
		return $this->base_url;
	}

	/**
	 * Set the base URL.
	 *
	 * @param string $base_url Base URL to set.
	 * @return void
	 */
	public function set_base_url( string $base_url ): void {
		$this->base_url = rtrim( $base_url, '/' );
	}

	/**
	 * Get the timeout.
	 *
	 * @return int Timeout in seconds.
	 */
	public function get_timeout(): int {
		return $this->timeout;
	}

	/**
	 * Set the timeout.
	 *
	 * @param int $timeout Timeout in seconds.
	 * @return void
	 */
	public function set_timeout( int $timeout ): void {
		$this->timeout = $timeout;
	}

	/**
	 * Get the maximum number of retries.
	 *
	 * @return int Maximum retries.
	 */
	public function get_max_retries(): int {
		return $this->max_retries;
	}

	/**
	 * Set the maximum number of retries.
	 *
	 * @param int $max_retries Maximum retries.
	 * @return void
	 */
	public function set_max_retries( int $max_retries ): void {
		$this->max_retries = max( 0, $max_retries );
	}

	/**
	 * Get the authentication handler.
	 *
	 * @return Authentication Authentication handler.
	 */
	public function get_authentication(): Authentication {
		return $this->authentication;
	}

	/**
	 * Set the authentication handler.
	 *
	 * @param Authentication $authentication Authentication handler.
	 * @return void
	 */
	public function set_authentication( Authentication $authentication ): void {
		$this->authentication = $authentication;
	}
}